#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const readline = require('readline');

const colors = {
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m',
  reset: '\x1b[0m'
};

function log(color, symbol, message) {
  console.log(`${color}${symbol}${colors.reset} ${message}`);
}

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

function askQuestion(query) {
  return new Promise(resolve => rl.question(query, resolve));
}

function askSecretQuestion(query) {
  return new Promise((resolve) => {
    const stdin = process.stdin;
    const stdout = process.stdout;

    let input = '';

    stdout.write(query);

    stdin.setRawMode(true);
    stdin.resume();
    stdin.setEncoding('utf8');

    const onData = (char) => {
      switch (char) {
        case '\n':
        case '\r':
        case '\u0004':
          stdin.setRawMode(false);
          stdin.pause();
          stdin.removeListener('data', onData);
          stdout.write('\n');
          resolve(input);
          break;
        case '\u0003':
          process.exit();
          break;
        case '\u007f':
          if (input.length > 0) {
            input = input.slice(0, -1);
          }
          break;
        default:
          input += char;
          break;
      }
    };

    stdin.on('data', onData);
  });
}

function extractEnvVariables(command, envConfig) {
  const variables = new Map();
  const regex = /\$\{([^}]+)\}/g;
  let match;

  while ((match = regex.exec(command)) !== null) {
    const varName = match[1];
    if (envConfig && envConfig[varName]) {
      variables.set(varName, envConfig[varName]);
    }
  }

  return variables;
}

function replaceEnvVariables(command, envValues) {
  let result = command;
  for (const [varName, value] of envValues.entries()) {
    result = result.replace(new RegExp(`\\$\\{${varName}\\}`, 'g'), value);
  }
  return result;
}

function maskEnvVariables(command, envValues) {
  let result = command;
  for (const [varName, value] of envValues.entries()) {
    const masked = '*'.repeat(8);
    result = result.replace(new RegExp(value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g'), masked);
  }
  return result;
}

async function installMcp(mcpName, mcpConfig) {
  console.log(`\n${colors.cyan}=== Installing MCP: ${mcpName} ===${colors.reset}`);

  const transport = mcpConfig.transport || 'stdio';
  const command = mcpConfig.command;
  const envConfig = mcpConfig.env || {};

  const envVariables = extractEnvVariables(command, envConfig);
  const envValues = new Map();

  if (envVariables.size > 0) {
    console.log(`${colors.blue}Required environment variables:${colors.reset}`);
    for (const [varName, placeholder] of envVariables.entries()) {
      const hasPlaceholder = placeholder.startsWith('${');
      if (hasPlaceholder) {
        const answer = await askSecretQuestion(`  ${varName}: `);
        envValues.set(varName, answer.trim());
      } else {
        envValues.set(varName, placeholder);
      }
    }
  }

  const finalCommand = replaceEnvVariables(command, envValues);
  const [mainCommand, ...args] = finalCommand.split(' ');
  const argsString = args.join(' ');

  const claudeCommand = `claude mcp add --transport ${transport} ${mcpName} -- ${mainCommand} ${argsString}`;
  const maskedCommand = maskEnvVariables(claudeCommand, envValues);

  console.log(`${colors.blue}Executing:${colors.reset} ${maskedCommand}\n`);

  let retry = true;
  while (retry) {
    try {
      execSync(claudeCommand, { stdio: 'inherit' });
      log(colors.green, '✓', `${mcpName} installed successfully`);
      return { success: true, mcpName };
    } catch (err) {
      log(colors.red, '✗', `Failed to install ${mcpName}`);
      console.log(`${colors.red}Error: ${err.message}${colors.reset}\n`);

      const answer = await askQuestion(`Retry or skip? (r/s): `);
      if (answer.toLowerCase() === 'r') {
        retry = true;
      } else {
        log(colors.yellow, '○', `Skipped ${mcpName}`);
        return { success: false, mcpName, skipped: true };
      }
    }
  }
}

async function installMcps() {
  console.log(`${colors.blue}=== Claude MCP Installation Tool ===${colors.reset}\n`);

  const mcpsDir = path.join(__dirname, 'mcps');

  if (!fs.existsSync(mcpsDir)) {
    log(colors.red, '✗', `MCPs directory not found: ${mcpsDir}`);
    process.exit(1);
  }

  const files = fs.readdirSync(mcpsDir).filter(file => file.endsWith('.json'));

  if (files.length === 0) {
    log(colors.yellow, '○', 'No MCP configuration files found in mcps/ directory');
    process.exit(0);
  }

  console.log(`${colors.blue}Found ${files.length} MCP configuration(s)${colors.reset}\n`);

  const results = {
    success: 0,
    failed: 0,
    skipped: 0
  };

  for (const file of files) {
    const filePath = path.join(mcpsDir, file);

    try {
      const content = fs.readFileSync(filePath, 'utf8');
      const config = JSON.parse(content);

      const mcpNames = Object.keys(config);

      for (const mcpName of mcpNames) {
        const result = await installMcp(mcpName, config[mcpName]);

        if (result.success) {
          results.success++;
        } else if (result.skipped) {
          results.skipped++;
        } else {
          results.failed++;
        }
      }
    } catch (err) {
      log(colors.red, '✗', `Error reading ${file}: ${err.message}`);
      results.failed++;
    }
  }

  console.log(`\n${colors.blue}=== Summary ===${colors.reset}`);
  console.log(`${colors.green}Installed:${colors.reset} ${results.success} MCP(s)`);
  console.log(`${colors.yellow}Skipped:${colors.reset}   ${results.skipped} MCP(s)`);
  if (results.failed > 0) {
    console.log(`${colors.red}Failed:${colors.reset}    ${results.failed} MCP(s)`);
  }

  console.log(`\n${colors.green}Done!${colors.reset}`);
  rl.close();
  process.exit(results.failed > 0 ? 1 : 0);
}

installMcps().catch(err => {
  console.error(`${colors.red}Unexpected error: ${err.message}${colors.reset}`);
  rl.close();
  process.exit(1);
});
