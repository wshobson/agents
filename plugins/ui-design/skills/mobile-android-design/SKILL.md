---
name: mobile-android-design
description: Master Material Design 3 and Jetpack Compose patterns for building native Android apps. Use when designing Android interfaces, implementing Compose UI, or following Google's Material Design guidelines.
---

# Android Mobile Design

Master Material Design 3 (Material You) and Jetpack Compose to build modern, adaptive Android applications that integrate seamlessly with the Android ecosystem.

## When to Use This Skill

- Designing Android app interfaces following Material Design 3
- Building Jetpack Compose UI and layouts
- Implementing Android navigation patterns (Navigation Compose)
- Creating adaptive layouts for phones, tablets, and foldables
- Using Material 3 theming with dynamic colors
- Building accessible Android interfaces
- Implementing Android-specific gestures and interactions
- Designing for different screen configurations

## Core Concepts

### 1. Material Design 3 Principles

**Personalization**: Dynamic color adapts UI to user's wallpaper
**Accessibility**: Tonal palettes ensure sufficient color contrast
**Large Screens**: Responsive layouts for tablets and foldables

**Material Components:**

- Cards, Buttons, FABs, Chips
- Navigation (rail, drawer, bottom nav)
- Text fields, Dialogs, Sheets
- Lists, Menus, Progress indicators

### 2. Jetpack Compose Layout System

**Column and Row:**

```kotlin
// Vertical arrangement with alignment
Column(
    modifier = Modifier.padding(16.dp),
    verticalArrangement = Arrangement.spacedBy(12.dp),
    horizontalAlignment = Alignment.Start
) {
    Text(
        text = "Title",
        style = MaterialTheme.typography.headlineSmall
    )
    Text(
        text = "Subtitle",
        style = MaterialTheme.typography.bodyMedium,
        color = MaterialTheme.colorScheme.onSurfaceVariant
    )
}

// Horizontal arrangement with weight
Row(
    modifier = Modifier.fillMaxWidth(),
    horizontalArrangement = Arrangement.SpaceBetween,
    verticalAlignment = Alignment.CenterVertically
) {
    Icon(Icons.Default.Star, contentDescription = null)
    Text("Featured")
    Spacer(modifier = Modifier.weight(1f))
    TextButton(onClick = {}) {
        Text("View All")
    }
}
```

**Lazy Lists and Grids:**

```kotlin
// Lazy column with sticky headers
LazyColumn {
    items.groupBy { it.category }.forEach { (category, categoryItems) ->
        stickyHeader {
            Text(
                text = category,
                modifier = Modifier
                    .fillMaxWidth()
                    .background(MaterialTheme.colorScheme.surface)
                    .padding(16.dp),
                style = MaterialTheme.typography.titleMedium
            )
        }
        items(categoryItems) { item ->
            ItemRow(item = item)
        }
    }
}

// Adaptive grid
LazyVerticalGrid(
    columns = GridCells.Adaptive(minSize = 150.dp),
    contentPadding = PaddingValues(16.dp),
    horizontalArrangement = Arrangement.spacedBy(12.dp),
    verticalArrangement = Arrangement.spacedBy(12.dp)
) {
    items(items) { item ->
        ItemCard(item = item)
    }
}
```

### 3. Navigation Patterns

**Bottom Navigation:**

```kotlin
@Composable
fun MainScreen() {
    val navController = rememberNavController()

    Scaffold(
        bottomBar = {
            NavigationBar {
                val navBackStackEntry by navController.currentBackStackEntryAsState()
                val currentDestination = navBackStackEntry?.destination

                NavigationDestination.entries.forEach { destination ->
                    NavigationBarItem(
                        icon = { Icon(destination.icon, contentDescription = null) },
                        label = { Text(destination.label) },
                        selected = currentDestination?.hierarchy?.any {
                            it.route == destination.route
                        } == true,
                        onClick = {
                            navController.navigate(destination.route) {
                                popUpTo(navController.graph.findStartDestination().id) {
                                    saveState = true
                                }
                                launchSingleTop = true
                                restoreState = true
                            }
                        }
                    )
                }
            }
        }
    ) { innerPadding ->
        NavHost(
            navController = navController,
            startDestination = NavigationDestination.Home.route,
            modifier = Modifier.padding(innerPadding)
        ) {
            composable(NavigationDestination.Home.route) { HomeScreen() }
            composable(NavigationDestination.Search.route) { SearchScreen() }
            composable(NavigationDestination.Profile.route) { ProfileScreen() }
        }
    }
}
```

**Navigation Drawer:**

```kotlin
@Composable
fun DrawerNavigation() {
    val drawerState = rememberDrawerState(DrawerValue.Closed)
    val scope = rememberCoroutineScope()

    ModalNavigationDrawer(
        drawerState = drawerState,
        drawerContent = {
            ModalDrawerSheet {
                Spacer(Modifier.height(12.dp))
                Text(
                    "App Name",
                    modifier = Modifier.padding(16.dp),
                    style = MaterialTheme.typography.titleLarge
                )
                HorizontalDivider()

                NavigationDrawerItem(
                    icon = { Icon(Icons.Default.Home, null) },
                    label = { Text("Home") },
                    selected = true,
                    onClick = { scope.launch { drawerState.close() } }
                )
                NavigationDrawerItem(
                    icon = { Icon(Icons.Default.Settings, null) },
                    label = { Text("Settings") },
                    selected = false,
                    onClick = { }
                )
            }
        }
    ) {
        Scaffold(
            topBar = {
                TopAppBar(
                    title = { Text("Home") },
                    navigationIcon = {
                        IconButton(onClick = { scope.launch { drawerState.open() } }) {
                            Icon(Icons.Default.Menu, contentDescription = "Menu")
                        }
                    }
                )
            }
        ) { innerPadding ->
            Content(modifier = Modifier.padding(innerPadding))
        }
    }
}
```

### 4. Material 3 Theming

**Color Scheme:**

```kotlin
// Dynamic color (Android 12+)
val dynamicColorScheme = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
    val context = LocalContext.current
    if (darkTheme) dynamicDarkColorScheme(context)
    else dynamicLightColorScheme(context)
} else {
    if (darkTheme) DarkColorScheme else LightColorScheme
}

// Custom color scheme
private val LightColorScheme = lightColorScheme(
    primary = Color(0xFF6750A4),
    onPrimary = Color.White,
    primaryContainer = Color(0xFFEADDFF),
    onPrimaryContainer = Color(0xFF21005D),
    secondary = Color(0xFF625B71),
    onSecondary = Color.White,
    tertiary = Color(0xFF7D5260),
    onTertiary = Color.White,
    surface = Color(0xFFFFFBFE),
    onSurface = Color(0xFF1C1B1F),
)
```

**Typography:**

```kotlin
val AppTypography = Typography(
    displayLarge = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Normal,
        fontSize = 57.sp,
        lineHeight = 64.sp
    ),
    headlineMedium = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Normal,
        fontSize = 28.sp,
        lineHeight = 36.sp
    ),
    titleLarge = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Normal,
        fontSize = 22.sp,
        lineHeight = 28.sp
    ),
    bodyLarge = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Normal,
        fontSize = 16.sp,
        lineHeight = 24.sp
    ),
    labelMedium = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Medium,
        fontSize = 12.sp,
        lineHeight = 16.sp
    )
)
```

### 5. Component Examples

**Cards:**

```kotlin
@Composable
fun FeatureCard(
    title: String,
    description: String,
    imageUrl: String,
    onClick: () -> Unit
) {
    Card(
        onClick = onClick,
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(16.dp),
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.surfaceVariant
        )
    ) {
        Column {
            AsyncImage(
                model = imageUrl,
                contentDescription = null,
                modifier = Modifier
                    .fillMaxWidth()
                    .height(180.dp),
                contentScale = ContentScale.Crop
            )
            Column(modifier = Modifier.padding(16.dp)) {
                Text(
                    text = title,
                    style = MaterialTheme.typography.titleMedium
                )
                Spacer(modifier = Modifier.height(8.dp))
                Text(
                    text = description,
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        }
    }
}
```

**Buttons:**

```kotlin
// Filled button (primary action)
Button(onClick = { }) {
    Text("Continue")
}

// Filled tonal button (secondary action)
FilledTonalButton(onClick = { }) {
    Icon(Icons.Default.Add, null)
    Spacer(Modifier.width(8.dp))
    Text("Add Item")
}

// Outlined button
OutlinedButton(onClick = { }) {
    Text("Cancel")
}

// Text button
TextButton(onClick = { }) {
    Text("Learn More")
}

// FAB
FloatingActionButton(
    onClick = { },
    containerColor = MaterialTheme.colorScheme.primaryContainer,
    contentColor = MaterialTheme.colorScheme.onPrimaryContainer
) {
    Icon(Icons.Default.Add, contentDescription = "Add")
}
```

## Quick Start Component

```kotlin
@Composable
fun ItemListCard(
    item: Item,
    onItemClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    Card(
        onClick = onItemClick,
        modifier = modifier.fillMaxWidth(),
        shape = RoundedCornerShape(12.dp)
    ) {
        Row(
            modifier = Modifier
                .padding(16.dp)
                .fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Box(
                modifier = Modifier
                    .size(48.dp)
                    .clip(CircleShape)
                    .background(MaterialTheme.colorScheme.primaryContainer),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = Icons.Default.Star,
                    contentDescription = null,
                    tint = MaterialTheme.colorScheme.onPrimaryContainer
                )
            }

            Spacer(modifier = Modifier.width(16.dp))

            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = item.title,
                    style = MaterialTheme.typography.titleMedium
                )
                Text(
                    text = item.subtitle,
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }

            Icon(
                imageVector = Icons.Default.ChevronRight,
                contentDescription = null,
                tint = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
    }
}
```

## Best Practices

1. **Use Material Theme**: Access colors via `MaterialTheme.colorScheme` for automatic dark mode support
2. **Support Dynamic Color**: Enable dynamic color on Android 12+ for personalization
3. **Adaptive Layouts**: Use `WindowSizeClass` for responsive designs
4. **Content Descriptions**: Add `contentDescription` to all interactive elements
5. **Touch Targets**: Minimum 48dp touch targets for accessibility
6. **State Hoisting**: Hoist state to make components reusable and testable
7. **Remember Properly**: Use `remember` and `rememberSaveable` appropriately
8. **Preview Annotations**: Add `@Preview` with different configurations

## Common Issues

- **Recomposition Issues**: Avoid passing unstable lambdas; use `remember`
- **State Loss**: Use `rememberSaveable` for configuration changes
- **Performance**: Use `LazyColumn` instead of `Column` for long lists
- **Theme Leaks**: Ensure `MaterialTheme` wraps all composables
- **Navigation Crashes**: Handle back press and deep links properly
- **Memory Leaks**: Cancel coroutines in `DisposableEffect`

## Resources

- [Material Design 3](https://m3.material.io/)
- [Jetpack Compose Documentation](https://developer.android.com/jetpack/compose)
- [Compose Samples](https://github.com/android/compose-samples)
- [Material 3 Compose](https://developer.android.com/jetpack/compose/designsystems/material3)
