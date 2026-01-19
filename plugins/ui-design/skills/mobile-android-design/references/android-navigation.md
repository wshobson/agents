# Android Navigation Patterns

## Navigation Compose Basics

### Setup and Dependencies

```kotlin
// build.gradle.kts
dependencies {
    implementation("androidx.navigation:navigation-compose:2.7.7")
    // For type-safe navigation (recommended)
    implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.6.3")
}
```

### Basic Navigation

```kotlin
@Serializable
object Home

@Serializable
data class Detail(val itemId: String)

@Serializable
object Settings

@Composable
fun AppNavigation() {
    val navController = rememberNavController()

    NavHost(
        navController = navController,
        startDestination = Home
    ) {
        composable<Home> {
            HomeScreen(
                onItemClick = { itemId ->
                    navController.navigate(Detail(itemId))
                },
                onSettingsClick = {
                    navController.navigate(Settings)
                }
            )
        }

        composable<Detail> { backStackEntry ->
            val detail: Detail = backStackEntry.toRoute()
            DetailScreen(
                itemId = detail.itemId,
                onBack = { navController.popBackStack() }
            )
        }

        composable<Settings> {
            SettingsScreen(
                onBack = { navController.popBackStack() }
            )
        }
    }
}
```

### Navigation with Arguments

```kotlin
// Type-safe routes with arguments
@Serializable
data class ProductDetail(
    val productId: String,
    val category: String,
    val fromSearch: Boolean = false
)

@Serializable
data class UserProfile(
    val userId: Long
)

@Composable
fun NavigationWithArgs() {
    val navController = rememberNavController()

    NavHost(navController = navController, startDestination = Home) {
        composable<Home> {
            HomeScreen(
                onProductClick = { productId, category ->
                    navController.navigate(
                        ProductDetail(
                            productId = productId,
                            category = category,
                            fromSearch = false
                        )
                    )
                }
            )
        }

        composable<ProductDetail> { backStackEntry ->
            val args: ProductDetail = backStackEntry.toRoute()
            ProductDetailScreen(
                productId = args.productId,
                category = args.category,
                showBackToSearch = args.fromSearch
            )
        }

        composable<UserProfile> { backStackEntry ->
            val args: UserProfile = backStackEntry.toRoute()
            UserProfileScreen(userId = args.userId)
        }
    }
}
```

## Bottom Navigation

### Standard Implementation

```kotlin
enum class BottomNavDestination(
    val route: Any,
    val icon: ImageVector,
    val label: String
) {
    HOME(Home, Icons.Default.Home, "Home"),
    SEARCH(Search, Icons.Default.Search, "Search"),
    FAVORITES(Favorites, Icons.Default.Favorite, "Favorites"),
    PROFILE(Profile, Icons.Default.Person, "Profile")
}

@Composable
fun MainScreenWithBottomNav() {
    val navController = rememberNavController()
    val navBackStackEntry by navController.currentBackStackEntryAsState()
    val currentDestination = navBackStackEntry?.destination

    Scaffold(
        bottomBar = {
            NavigationBar {
                BottomNavDestination.entries.forEach { destination ->
                    NavigationBarItem(
                        icon = {
                            Icon(destination.icon, contentDescription = destination.label)
                        },
                        label = { Text(destination.label) },
                        selected = currentDestination?.hasRoute(destination.route::class) == true,
                        onClick = {
                            navController.navigate(destination.route) {
                                // Pop up to start destination to avoid building up stack
                                popUpTo(navController.graph.findStartDestination().id) {
                                    saveState = true
                                }
                                // Avoid multiple copies of same destination
                                launchSingleTop = true
                                // Restore state when reselecting
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
            startDestination = Home,
            modifier = Modifier.padding(innerPadding)
        ) {
            composable<Home> { HomeScreen() }
            composable<Search> { SearchScreen() }
            composable<Favorites> { FavoritesScreen() }
            composable<Profile> { ProfileScreen() }
        }
    }
}
```

### Bottom Nav with Badges

```kotlin
@Composable
fun BottomNavWithBadges(
    cartCount: Int,
    notificationCount: Int
) {
    NavigationBar {
        NavigationBarItem(
            icon = { Icon(Icons.Default.Home, null) },
            label = { Text("Home") },
            selected = true,
            onClick = { }
        )

        NavigationBarItem(
            icon = {
                BadgedBox(
                    badge = {
                        if (cartCount > 0) {
                            Badge { Text("$cartCount") }
                        }
                    }
                ) {
                    Icon(Icons.Default.ShoppingCart, null)
                }
            },
            label = { Text("Cart") },
            selected = false,
            onClick = { }
        )

        NavigationBarItem(
            icon = {
                BadgedBox(
                    badge = {
                        if (notificationCount > 0) {
                            Badge {
                                Text(
                                    if (notificationCount > 99) "99+"
                                    else "$notificationCount"
                                )
                            }
                        }
                    }
                ) {
                    Icon(Icons.Default.Notifications, null)
                }
            },
            label = { Text("Alerts") },
            selected = false,
            onClick = { }
        )
    }
}
```

## Navigation Drawer

### Modal Navigation Drawer

```kotlin
@Composable
fun ModalDrawerNavigation() {
    val drawerState = rememberDrawerState(initialValue = DrawerValue.Closed)
    val scope = rememberCoroutineScope()
    var selectedItem by remember { mutableStateOf(0) }

    val items = listOf(
        DrawerItem(Icons.Default.Home, "Home"),
        DrawerItem(Icons.Default.Settings, "Settings"),
        DrawerItem(Icons.Default.Info, "About"),
        DrawerItem(Icons.Default.Help, "Help")
    )

    ModalNavigationDrawer(
        drawerState = drawerState,
        drawerContent = {
            ModalDrawerSheet {
                // Header
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(180.dp)
                        .background(MaterialTheme.colorScheme.primaryContainer),
                    contentAlignment = Alignment.BottomStart
                ) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        AsyncImage(
                            model = "avatar_url",
                            contentDescription = "Profile",
                            modifier = Modifier
                                .size(64.dp)
                                .clip(CircleShape)
                        )
                        Spacer(Modifier.height(8.dp))
                        Text(
                            "John Doe",
                            style = MaterialTheme.typography.titleMedium
                        )
                        Text(
                            "john@example.com",
                            style = MaterialTheme.typography.bodySmall
                        )
                    }
                }

                Spacer(Modifier.height(12.dp))

                // Navigation items
                items.forEachIndexed { index, item ->
                    NavigationDrawerItem(
                        icon = { Icon(item.icon, contentDescription = null) },
                        label = { Text(item.label) },
                        selected = index == selectedItem,
                        onClick = {
                            selectedItem = index
                            scope.launch { drawerState.close() }
                        },
                        modifier = Modifier.padding(NavigationDrawerItemDefaults.ItemPadding)
                    )
                }

                Spacer(Modifier.weight(1f))

                // Footer
                HorizontalDivider()
                NavigationDrawerItem(
                    icon = { Icon(Icons.Default.Logout, null) },
                    label = { Text("Sign Out") },
                    selected = false,
                    onClick = { },
                    modifier = Modifier.padding(NavigationDrawerItemDefaults.ItemPadding)
                )
                Spacer(Modifier.height(12.dp))
            }
        }
    ) {
        Scaffold(
            topBar = {
                TopAppBar(
                    title = { Text(items[selectedItem].label) },
                    navigationIcon = {
                        IconButton(onClick = { scope.launch { drawerState.open() } }) {
                            Icon(Icons.Default.Menu, "Open drawer")
                        }
                    }
                )
            }
        ) { padding ->
            Content(modifier = Modifier.padding(padding))
        }
    }
}

data class DrawerItem(val icon: ImageVector, val label: String)
```

### Permanent Navigation Drawer (Tablets)

```kotlin
@Composable
fun PermanentDrawerLayout() {
    PermanentNavigationDrawer(
        drawerContent = {
            PermanentDrawerSheet(
                modifier = Modifier.width(240.dp)
            ) {
                Spacer(Modifier.height(12.dp))
                Text(
                    "App Name",
                    modifier = Modifier.padding(16.dp),
                    style = MaterialTheme.typography.titleLarge
                )
                HorizontalDivider()

                drawerItems.forEach { item ->
                    NavigationDrawerItem(
                        icon = { Icon(item.icon, null) },
                        label = { Text(item.label) },
                        selected = item == selectedItem,
                        onClick = { selectedItem = item },
                        modifier = Modifier.padding(horizontal = 12.dp)
                    )
                }
            }
        }
    ) {
        // Main content takes remaining space
        MainContent()
    }
}
```

## Navigation Rail

```kotlin
@Composable
fun NavigationRailLayout() {
    var selectedItem by remember { mutableStateOf(0) }

    Row(modifier = Modifier.fillMaxSize()) {
        NavigationRail(
            header = {
                FloatingActionButton(
                    onClick = { },
                    elevation = FloatingActionButtonDefaults.bottomAppBarFabElevation()
                ) {
                    Icon(Icons.Default.Add, "Create")
                }
            }
        ) {
            Spacer(Modifier.weight(1f))

            railItems.forEachIndexed { index, item ->
                NavigationRailItem(
                    icon = { Icon(item.icon, null) },
                    label = { Text(item.label) },
                    selected = selectedItem == index,
                    onClick = { selectedItem = index }
                )
            }

            Spacer(Modifier.weight(1f))
        }

        // Main content
        Box(
            modifier = Modifier
                .weight(1f)
                .fillMaxHeight()
        ) {
            when (selectedItem) {
                0 -> HomeContent()
                1 -> SearchContent()
                2 -> ProfileContent()
            }
        }
    }
}
```

## Deep Linking

### Basic Deep Link Setup

```kotlin
// In AndroidManifest.xml
// <intent-filter>
//     <action android:name="android.intent.action.VIEW" />
//     <category android:name="android.intent.category.DEFAULT" />
//     <category android:name="android.intent.category.BROWSABLE" />
//     <data android:scheme="myapp" />
//     <data android:scheme="https" android:host="myapp.com" />
// </intent-filter>

@Composable
fun DeepLinkNavigation() {
    val navController = rememberNavController()

    NavHost(
        navController = navController,
        startDestination = Home
    ) {
        composable<Home> {
            HomeScreen()
        }

        composable<ProductDetail>(
            deepLinks = listOf(
                navDeepLink<ProductDetail>(
                    basePath = "https://myapp.com/product"
                ),
                navDeepLink<ProductDetail>(
                    basePath = "myapp://product"
                )
            )
        ) { backStackEntry ->
            val args: ProductDetail = backStackEntry.toRoute()
            ProductDetailScreen(productId = args.productId)
        }

        composable<UserProfile>(
            deepLinks = listOf(
                navDeepLink<UserProfile>(
                    basePath = "https://myapp.com/user"
                )
            )
        ) { backStackEntry ->
            val args: UserProfile = backStackEntry.toRoute()
            UserProfileScreen(userId = args.userId)
        }
    }
}
```

### Handling Intent in Activity

```kotlin
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        setContent {
            AppTheme {
                val navController = rememberNavController()

                // Handle deep link from intent
                LaunchedEffect(Unit) {
                    intent?.data?.let { uri ->
                        navController.handleDeepLink(intent)
                    }
                }

                AppNavigation(navController = navController)
            }
        }
    }

    override fun onNewIntent(intent: Intent) {
        super.onNewIntent(intent)
        // Handle new intents when activity is already running
        setIntent(intent)
    }
}
```

## Nested Navigation

```kotlin
@Composable
fun NestedNavigation() {
    val navController = rememberNavController()

    NavHost(navController = navController, startDestination = MainGraph) {
        // Main graph with bottom navigation
        navigation<MainGraph>(startDestination = Home) {
            composable<Home> {
                HomeScreen(
                    onItemClick = { navController.navigate(Detail(it)) }
                )
            }
            composable<Search> { SearchScreen() }
            composable<Profile> {
                ProfileScreen(
                    onSettingsClick = { navController.navigate(SettingsGraph) }
                )
            }
        }

        // Nested detail graph
        composable<Detail> { backStackEntry ->
            val args: Detail = backStackEntry.toRoute()
            DetailScreen(itemId = args.itemId)
        }

        // Separate settings graph (full screen, no bottom nav)
        navigation<SettingsGraph>(startDestination = SettingsMain) {
            composable<SettingsMain> {
                SettingsScreen(
                    onAccountClick = { navController.navigate(AccountSettings) },
                    onNotificationsClick = { navController.navigate(NotificationSettings) }
                )
            }
            composable<AccountSettings> { AccountSettingsScreen() }
            composable<NotificationSettings> { NotificationSettingsScreen() }
        }
    }
}

@Serializable object MainGraph
@Serializable object SettingsGraph
@Serializable object SettingsMain
@Serializable object AccountSettings
@Serializable object NotificationSettings
```

## Navigation State Management

### ViewModel Integration

```kotlin
@HiltViewModel
class NavigationViewModel @Inject constructor(
    private val savedStateHandle: SavedStateHandle
) : ViewModel() {

    private val _navigationEvents = MutableSharedFlow<NavigationEvent>()
    val navigationEvents = _navigationEvents.asSharedFlow()

    fun navigateToDetail(itemId: String) {
        viewModelScope.launch {
            _navigationEvents.emit(NavigationEvent.NavigateToDetail(itemId))
        }
    }

    fun navigateBack() {
        viewModelScope.launch {
            _navigationEvents.emit(NavigationEvent.NavigateBack)
        }
    }
}

sealed class NavigationEvent {
    data class NavigateToDetail(val itemId: String) : NavigationEvent()
    object NavigateBack : NavigationEvent()
}

@Composable
fun NavigationHandler(
    navController: NavHostController,
    viewModel: NavigationViewModel = hiltViewModel()
) {
    LaunchedEffect(Unit) {
        viewModel.navigationEvents.collect { event ->
            when (event) {
                is NavigationEvent.NavigateToDetail -> {
                    navController.navigate(Detail(event.itemId))
                }
                NavigationEvent.NavigateBack -> {
                    navController.popBackStack()
                }
            }
        }
    }
}
```

### Back Handler

```kotlin
@Composable
fun ScreenWithBackHandler(
    onBack: () -> Unit
) {
    var showExitDialog by remember { mutableStateOf(false) }

    // Intercept back press
    BackHandler {
        showExitDialog = true
    }

    if (showExitDialog) {
        AlertDialog(
            onDismissRequest = { showExitDialog = false },
            title = { Text("Exit App?") },
            text = { Text("Are you sure you want to exit?") },
            confirmButton = {
                TextButton(onClick = onBack) {
                    Text("Exit")
                }
            },
            dismissButton = {
                TextButton(onClick = { showExitDialog = false }) {
                    Text("Cancel")
                }
            }
        )
    }

    // Screen content
    Content()
}
```

## Navigation Animations

```kotlin
@Composable
fun AnimatedNavigation() {
    val navController = rememberNavController()

    NavHost(
        navController = navController,
        startDestination = Home,
        enterTransition = {
            slideIntoContainer(
                towards = AnimatedContentTransitionScope.SlideDirection.Left,
                animationSpec = tween(300)
            )
        },
        exitTransition = {
            slideOutOfContainer(
                towards = AnimatedContentTransitionScope.SlideDirection.Left,
                animationSpec = tween(300)
            )
        },
        popEnterTransition = {
            slideIntoContainer(
                towards = AnimatedContentTransitionScope.SlideDirection.Right,
                animationSpec = tween(300)
            )
        },
        popExitTransition = {
            slideOutOfContainer(
                towards = AnimatedContentTransitionScope.SlideDirection.Right,
                animationSpec = tween(300)
            )
        }
    ) {
        composable<Home> {
            HomeScreen()
        }

        composable<Detail>(
            // Custom transition for specific route
            enterTransition = {
                fadeIn(animationSpec = tween(500)) +
                    scaleIn(initialScale = 0.9f, animationSpec = tween(500))
            },
            exitTransition = {
                fadeOut(animationSpec = tween(500))
            }
        ) {
            DetailScreen()
        }
    }
}
```
