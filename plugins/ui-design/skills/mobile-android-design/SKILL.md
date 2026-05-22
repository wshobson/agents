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

## Detailed section: Core Concepts

Originally a 9201-byte section in this SKILL.md. Moved to `references/details.md` to fit Codex's 8 KB skill body cap.

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
