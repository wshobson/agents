# Material Design 3 Theming

## Color System

### Dynamic Color (Material You)

```kotlin
@Composable
fun AppTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    dynamicColor: Boolean = true,
    content: @Composable () -> Unit
) {
    val colorScheme = when {
        dynamicColor && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S -> {
            val context = LocalContext.current
            if (darkTheme) dynamicDarkColorScheme(context)
            else dynamicLightColorScheme(context)
        }
        darkTheme -> DarkColorScheme
        else -> LightColorScheme
    }

    MaterialTheme(
        colorScheme = colorScheme,
        typography = AppTypography,
        shapes = AppShapes,
        content = content
    )
}
```

### Custom Color Scheme

```kotlin
// Define color palette
val md_theme_light_primary = Color(0xFF6750A4)
val md_theme_light_onPrimary = Color(0xFFFFFFFF)
val md_theme_light_primaryContainer = Color(0xFFEADDFF)
val md_theme_light_onPrimaryContainer = Color(0xFF21005D)
val md_theme_light_secondary = Color(0xFF625B71)
val md_theme_light_onSecondary = Color(0xFFFFFFFF)
val md_theme_light_secondaryContainer = Color(0xFFE8DEF8)
val md_theme_light_onSecondaryContainer = Color(0xFF1D192B)
val md_theme_light_tertiary = Color(0xFF7D5260)
val md_theme_light_onTertiary = Color(0xFFFFFFFF)
val md_theme_light_tertiaryContainer = Color(0xFFFFD8E4)
val md_theme_light_onTertiaryContainer = Color(0xFF31111D)
val md_theme_light_error = Color(0xFFB3261E)
val md_theme_light_onError = Color(0xFFFFFFFF)
val md_theme_light_errorContainer = Color(0xFFF9DEDC)
val md_theme_light_onErrorContainer = Color(0xFF410E0B)
val md_theme_light_background = Color(0xFFFFFBFE)
val md_theme_light_onBackground = Color(0xFF1C1B1F)
val md_theme_light_surface = Color(0xFFFFFBFE)
val md_theme_light_onSurface = Color(0xFF1C1B1F)
val md_theme_light_surfaceVariant = Color(0xFFE7E0EC)
val md_theme_light_onSurfaceVariant = Color(0xFF49454F)
val md_theme_light_outline = Color(0xFF79747E)
val md_theme_light_outlineVariant = Color(0xFFCAC4D0)

val LightColorScheme = lightColorScheme(
    primary = md_theme_light_primary,
    onPrimary = md_theme_light_onPrimary,
    primaryContainer = md_theme_light_primaryContainer,
    onPrimaryContainer = md_theme_light_onPrimaryContainer,
    secondary = md_theme_light_secondary,
    onSecondary = md_theme_light_onSecondary,
    secondaryContainer = md_theme_light_secondaryContainer,
    onSecondaryContainer = md_theme_light_onSecondaryContainer,
    tertiary = md_theme_light_tertiary,
    onTertiary = md_theme_light_onTertiary,
    tertiaryContainer = md_theme_light_tertiaryContainer,
    onTertiaryContainer = md_theme_light_onTertiaryContainer,
    error = md_theme_light_error,
    onError = md_theme_light_onError,
    errorContainer = md_theme_light_errorContainer,
    onErrorContainer = md_theme_light_onErrorContainer,
    background = md_theme_light_background,
    onBackground = md_theme_light_onBackground,
    surface = md_theme_light_surface,
    onSurface = md_theme_light_onSurface,
    surfaceVariant = md_theme_light_surfaceVariant,
    onSurfaceVariant = md_theme_light_onSurfaceVariant,
    outline = md_theme_light_outline,
    outlineVariant = md_theme_light_outlineVariant
)

// Dark colors follow the same pattern
val DarkColorScheme = darkColorScheme(
    primary = md_theme_dark_primary,
    // ... other colors
)
```

### Color Roles Usage

```kotlin
@Composable
fun ColorRolesExample() {
    Column(
        modifier = Modifier.padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        // Primary - Key actions, FABs
        Button(onClick = { }) {
            Text("Primary Action")
        }

        // Primary Container - Less prominent containers
        Surface(
            color = MaterialTheme.colorScheme.primaryContainer,
            shape = RoundedCornerShape(12.dp)
        ) {
            Text(
                "Primary Container",
                modifier = Modifier.padding(16.dp),
                color = MaterialTheme.colorScheme.onPrimaryContainer
            )
        }

        // Secondary - Less prominent actions
        FilledTonalButton(onClick = { }) {
            Text("Secondary Action")
        }

        // Tertiary - Contrast accents
        Badge(
            containerColor = MaterialTheme.colorScheme.tertiaryContainer,
            contentColor = MaterialTheme.colorScheme.onTertiaryContainer
        ) {
            Text("New")
        }

        // Error - Destructive actions
        Button(
            onClick = { },
            colors = ButtonDefaults.buttonColors(
                containerColor = MaterialTheme.colorScheme.error
            )
        ) {
            Text("Delete")
        }

        // Surface variants
        Surface(
            color = MaterialTheme.colorScheme.surfaceVariant,
            shape = RoundedCornerShape(8.dp)
        ) {
            Text(
                "Surface Variant",
                modifier = Modifier.padding(16.dp),
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
    }
}
```

### Extended Colors

```kotlin
// Custom semantic colors beyond M3 defaults
data class ExtendedColors(
    val success: Color,
    val onSuccess: Color,
    val successContainer: Color,
    val onSuccessContainer: Color,
    val warning: Color,
    val onWarning: Color,
    val warningContainer: Color,
    val onWarningContainer: Color
)

val LocalExtendedColors = staticCompositionLocalOf {
    ExtendedColors(
        success = Color(0xFF4CAF50),
        onSuccess = Color.White,
        successContainer = Color(0xFFE8F5E9),
        onSuccessContainer = Color(0xFF1B5E20),
        warning = Color(0xFFFF9800),
        onWarning = Color.White,
        warningContainer = Color(0xFFFFF3E0),
        onWarningContainer = Color(0xFFE65100)
    )
}

@Composable
fun AppTheme(
    content: @Composable () -> Unit
) {
    val extendedColors = ExtendedColors(
        // ... define colors based on light/dark theme
    )

    CompositionLocalProvider(
        LocalExtendedColors provides extendedColors
    ) {
        MaterialTheme(
            colorScheme = colorScheme,
            content = content
        )
    }
}

// Usage
@Composable
fun SuccessBanner() {
    val extendedColors = LocalExtendedColors.current

    Surface(
        color = extendedColors.successContainer,
        shape = RoundedCornerShape(8.dp)
    ) {
        Row(
            modifier = Modifier.padding(16.dp),
            horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            Icon(
                Icons.Default.CheckCircle,
                contentDescription = null,
                tint = extendedColors.success
            )
            Text(
                "Operation successful!",
                color = extendedColors.onSuccessContainer
            )
        }
    }
}
```

## Typography

### Material 3 Type Scale

```kotlin
val AppTypography = Typography(
    // Display styles - Hero text, large numerals
    displayLarge = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Normal,
        fontSize = 57.sp,
        lineHeight = 64.sp,
        letterSpacing = (-0.25).sp
    ),
    displayMedium = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Normal,
        fontSize = 45.sp,
        lineHeight = 52.sp,
        letterSpacing = 0.sp
    ),
    displaySmall = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Normal,
        fontSize = 36.sp,
        lineHeight = 44.sp,
        letterSpacing = 0.sp
    ),

    // Headline styles - High emphasis, short text
    headlineLarge = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Normal,
        fontSize = 32.sp,
        lineHeight = 40.sp,
        letterSpacing = 0.sp
    ),
    headlineMedium = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Normal,
        fontSize = 28.sp,
        lineHeight = 36.sp,
        letterSpacing = 0.sp
    ),
    headlineSmall = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Normal,
        fontSize = 24.sp,
        lineHeight = 32.sp,
        letterSpacing = 0.sp
    ),

    // Title styles - Medium emphasis headers
    titleLarge = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Normal,
        fontSize = 22.sp,
        lineHeight = 28.sp,
        letterSpacing = 0.sp
    ),
    titleMedium = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Medium,
        fontSize = 16.sp,
        lineHeight = 24.sp,
        letterSpacing = 0.15.sp
    ),
    titleSmall = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Medium,
        fontSize = 14.sp,
        lineHeight = 20.sp,
        letterSpacing = 0.1.sp
    ),

    // Body styles - Long-form text
    bodyLarge = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Normal,
        fontSize = 16.sp,
        lineHeight = 24.sp,
        letterSpacing = 0.5.sp
    ),
    bodyMedium = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Normal,
        fontSize = 14.sp,
        lineHeight = 20.sp,
        letterSpacing = 0.25.sp
    ),
    bodySmall = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Normal,
        fontSize = 12.sp,
        lineHeight = 16.sp,
        letterSpacing = 0.4.sp
    ),

    // Label styles - Buttons, chips, navigation
    labelLarge = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Medium,
        fontSize = 14.sp,
        lineHeight = 20.sp,
        letterSpacing = 0.1.sp
    ),
    labelMedium = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Medium,
        fontSize = 12.sp,
        lineHeight = 16.sp,
        letterSpacing = 0.5.sp
    ),
    labelSmall = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Medium,
        fontSize = 11.sp,
        lineHeight = 16.sp,
        letterSpacing = 0.5.sp
    )
)
```

### Custom Fonts

```kotlin
// Load custom fonts
val Inter = FontFamily(
    Font(R.font.inter_regular, FontWeight.Normal),
    Font(R.font.inter_medium, FontWeight.Medium),
    Font(R.font.inter_semibold, FontWeight.SemiBold),
    Font(R.font.inter_bold, FontWeight.Bold)
)

val AppTypography = Typography(
    displayLarge = TextStyle(
        fontFamily = Inter,
        fontWeight = FontWeight.Normal,
        fontSize = 57.sp,
        lineHeight = 64.sp
    ),
    // Apply to all styles...
)

// Variable fonts (Android 12+)
val InterVariable = FontFamily(
    Font(
        R.font.inter_variable,
        variationSettings = FontVariation.Settings(
            FontVariation.weight(400)
        )
    )
)
```

## Shape System

### Material 3 Shapes

```kotlin
val AppShapes = Shapes(
    // Extra small - Chips, small buttons
    extraSmall = RoundedCornerShape(4.dp),

    // Small - Text fields, small cards
    small = RoundedCornerShape(8.dp),

    // Medium - Cards, dialogs
    medium = RoundedCornerShape(12.dp),

    // Large - Large cards, bottom sheets
    large = RoundedCornerShape(16.dp),

    // Extra large - Full-screen dialogs
    extraLarge = RoundedCornerShape(28.dp)
)
```

### Custom Shape Usage

```kotlin
@Composable
fun ShapedComponents() {
    Column(
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        // Small shape for text field
        OutlinedTextField(
            value = "",
            onValueChange = {},
            shape = MaterialTheme.shapes.small,
            label = { Text("Input") }
        )

        // Medium shape for cards
        Card(
            shape = MaterialTheme.shapes.medium
        ) {
            Text("Card content", modifier = Modifier.padding(16.dp))
        }

        // Large shape for prominent containers
        Surface(
            shape = MaterialTheme.shapes.large,
            color = MaterialTheme.colorScheme.primaryContainer
        ) {
            Text("Featured", modifier = Modifier.padding(24.dp))
        }

        // Custom asymmetric shape
        Surface(
            shape = RoundedCornerShape(
                topStart = 24.dp,
                topEnd = 24.dp,
                bottomStart = 0.dp,
                bottomEnd = 0.dp
            ),
            color = MaterialTheme.colorScheme.surface
        ) {
            Text("Bottom sheet style", modifier = Modifier.padding(16.dp))
        }
    }
}
```

## Elevation and Shadows

### Tonal Elevation

```kotlin
@Composable
fun ElevationExample() {
    Column(
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        // Level 0 - No elevation
        Surface(
            tonalElevation = 0.dp,
            shadowElevation = 0.dp
        ) {
            Text("Level 0", modifier = Modifier.padding(16.dp))
        }

        // Level 1 - Low emphasis surfaces
        Surface(
            tonalElevation = 1.dp,
            shadowElevation = 1.dp
        ) {
            Text("Level 1", modifier = Modifier.padding(16.dp))
        }

        // Level 2 - Cards, switches
        Surface(
            tonalElevation = 3.dp,
            shadowElevation = 2.dp
        ) {
            Text("Level 2", modifier = Modifier.padding(16.dp))
        }

        // Level 3 - Navigation components
        Surface(
            tonalElevation = 6.dp,
            shadowElevation = 4.dp
        ) {
            Text("Level 3", modifier = Modifier.padding(16.dp))
        }

        // Level 4 - Navigation rail
        Surface(
            tonalElevation = 8.dp,
            shadowElevation = 6.dp
        ) {
            Text("Level 4", modifier = Modifier.padding(16.dp))
        }

        // Level 5 - FAB
        Surface(
            tonalElevation = 12.dp,
            shadowElevation = 8.dp
        ) {
            Text("Level 5", modifier = Modifier.padding(16.dp))
        }
    }
}
```

## Responsive Design

### Window Size Classes

```kotlin
@Composable
fun AdaptiveLayout() {
    val windowSizeClass = calculateWindowSizeClass(LocalContext.current as Activity)

    when (windowSizeClass.widthSizeClass) {
        WindowWidthSizeClass.Compact -> {
            // Phone portrait - Single column, bottom nav
            CompactLayout()
        }
        WindowWidthSizeClass.Medium -> {
            // Tablet portrait, phone landscape - Navigation rail
            MediumLayout()
        }
        WindowWidthSizeClass.Expanded -> {
            // Tablet landscape, desktop - Navigation drawer, multi-pane
            ExpandedLayout()
        }
    }
}

@Composable
fun CompactLayout() {
    Scaffold(
        bottomBar = { NavigationBar { /* items */ } }
    ) { padding ->
        Content(modifier = Modifier.padding(padding))
    }
}

@Composable
fun MediumLayout() {
    Row {
        NavigationRail { /* items */ }
        Content(modifier = Modifier.weight(1f))
    }
}

@Composable
fun ExpandedLayout() {
    PermanentNavigationDrawer(
        drawerContent = {
            PermanentDrawerSheet { /* items */ }
        }
    ) {
        Row {
            ListPane(modifier = Modifier.weight(0.4f))
            DetailPane(modifier = Modifier.weight(0.6f))
        }
    }
}
```

### Foldable Support

```kotlin
@Composable
fun FoldableAwareLayout() {
    val foldingFeature = LocalFoldingFeature.current

    when {
        foldingFeature?.state == FoldingFeature.State.HALF_OPENED -> {
            // Device is half-folded (tabletop mode)
            TwoHingeLayout(
                top = { CameraPreview() },
                bottom = { CameraControls() }
            )
        }
        foldingFeature?.orientation == FoldingFeature.Orientation.VERTICAL -> {
            // Vertical fold (book mode)
            TwoPaneLayout(
                first = { NavigationPane() },
                second = { ContentPane() }
            )
        }
        else -> {
            // Regular or fully opened
            SinglePaneLayout()
        }
    }
}
```
