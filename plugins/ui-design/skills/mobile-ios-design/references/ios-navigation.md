# iOS Navigation Patterns

## NavigationStack (iOS 16+)

### Basic Navigation

```swift
struct BasicNavigationView: View {
    var body: some View {
        NavigationStack {
            List(items) { item in
                NavigationLink(item.title, value: item)
            }
            .navigationTitle("Items")
            .navigationDestination(for: Item.self) { item in
                ItemDetailView(item: item)
            }
        }
    }
}
```

### Programmatic Navigation

```swift
struct ProgrammaticNavigationView: View {
    @State private var path = NavigationPath()

    var body: some View {
        NavigationStack(path: $path) {
            VStack(spacing: 20) {
                Button("Go to Settings") {
                    path.append(Destination.settings)
                }

                Button("Go to Profile") {
                    path.append(Destination.profile)
                }

                Button("Deep Link to Item 123") {
                    path.append(Destination.settings)
                    path.append(Destination.itemDetail(id: 123))
                }
            }
            .navigationTitle("Home")
            .navigationDestination(for: Destination.self) { destination in
                switch destination {
                case .settings:
                    SettingsView()
                case .profile:
                    ProfileView()
                case .itemDetail(let id):
                    ItemDetailView(itemId: id)
                }
            }
        }
    }

    enum Destination: Hashable {
        case settings
        case profile
        case itemDetail(id: Int)
    }
}
```

### Navigation State Persistence

```swift
struct PersistentNavigationView: View {
    @SceneStorage("navigationPath") private var pathData: Data?
    @State private var path = NavigationPath()

    var body: some View {
        NavigationStack(path: $path) {
            ContentView()
                .navigationDestination(for: Item.self) { item in
                    ItemDetailView(item: item)
                }
        }
        .onAppear {
            restorePath()
        }
        .onChange(of: path) { _, newPath in
            savePath(newPath)
        }
    }

    private func savePath(_ path: NavigationPath) {
        guard let representation = path.codable else { return }
        pathData = try? JSONEncoder().encode(representation)
    }

    private func restorePath() {
        guard let data = pathData,
              let representation = try? JSONDecoder().decode(
                NavigationPath.CodableRepresentation.self,
                from: data
              ) else { return }
        path = NavigationPath(representation)
    }
}
```

## NavigationSplitView

### Two-Column Layout

```swift
struct TwoColumnView: View {
    @State private var selectedCategory: Category?
    @State private var columnVisibility: NavigationSplitViewVisibility = .all

    var body: some View {
        NavigationSplitView(columnVisibility: $columnVisibility) {
            // Sidebar
            List(categories, selection: $selectedCategory) { category in
                NavigationLink(value: category) {
                    Label(category.name, systemImage: category.icon)
                }
            }
            .navigationTitle("Categories")
        } detail: {
            // Detail
            if let category = selectedCategory {
                CategoryDetailView(category: category)
            } else {
                ContentUnavailableView(
                    "Select a Category",
                    systemImage: "sidebar.leading"
                )
            }
        }
        .navigationSplitViewStyle(.balanced)
    }
}
```

### Three-Column Layout

```swift
struct ThreeColumnView: View {
    @State private var selectedFolder: Folder?
    @State private var selectedDocument: Document?

    var body: some View {
        NavigationSplitView {
            // Sidebar
            List(folders, selection: $selectedFolder) { folder in
                NavigationLink(value: folder) {
                    Label(folder.name, systemImage: "folder")
                }
            }
            .navigationTitle("Folders")
        } content: {
            // Content column
            if let folder = selectedFolder {
                List(folder.documents, selection: $selectedDocument) { document in
                    NavigationLink(value: document) {
                        DocumentRow(document: document)
                    }
                }
                .navigationTitle(folder.name)
            } else {
                Text("Select a folder")
            }
        } detail: {
            // Detail column
            if let document = selectedDocument {
                DocumentDetailView(document: document)
            } else {
                ContentUnavailableView(
                    "Select a Document",
                    systemImage: "doc"
                )
            }
        }
    }
}
```

## Sheet Navigation

### Modal Sheets

```swift
struct SheetNavigationView: View {
    @State private var showSettings = false
    @State private var showNewItem = false
    @State private var editingItem: Item?

    var body: some View {
        NavigationStack {
            ContentView()
                .toolbar {
                    ToolbarItem(placement: .primaryAction) {
                        Button("Add", systemImage: "plus") {
                            showNewItem = true
                        }
                    }
                    ToolbarItem(placement: .topBarLeading) {
                        Button("Settings", systemImage: "gear") {
                            showSettings = true
                        }
                    }
                }
        }
        // Boolean-based sheet
        .sheet(isPresented: $showSettings) {
            SettingsSheet()
        }
        // Boolean-based fullscreen cover
        .fullScreenCover(isPresented: $showNewItem) {
            NewItemView()
        }
        // Item-based sheet
        .sheet(item: $editingItem) { item in
            EditItemSheet(item: item)
        }
    }
}
```

### Sheet with Navigation

```swift
struct NavigableSheet: View {
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        NavigationStack {
            Form {
                Section("General") {
                    NavigationLink("Account") {
                        AccountSettingsView()
                    }
                    NavigationLink("Notifications") {
                        NotificationSettingsView()
                    }
                }

                Section("Advanced") {
                    NavigationLink("Privacy") {
                        PrivacySettingsView()
                    }
                }
            }
            .navigationTitle("Settings")
            .toolbar {
                ToolbarItem(placement: .confirmationAction) {
                    Button("Done") {
                        dismiss()
                    }
                }
            }
        }
    }
}
```

### Sheet Customization

```swift
struct CustomSheetView: View {
    @State private var showSheet = false

    var body: some View {
        Button("Show Sheet") {
            showSheet = true
        }
        .sheet(isPresented: $showSheet) {
            SheetContent()
                // Available detents
                .presentationDetents([
                    .medium,
                    .large,
                    .height(200),
                    .fraction(0.75)
                ])
                // Selected detent binding
                .presentationDetents([.medium, .large], selection: $selectedDetent)
                // Drag indicator visibility
                .presentationDragIndicator(.visible)
                // Corner radius
                .presentationCornerRadius(24)
                // Background interaction
                .presentationBackgroundInteraction(.enabled(upThrough: .medium))
                // Prevent interactive dismiss
                .interactiveDismissDisabled(hasUnsavedChanges)
        }
    }
}
```

## Tab Navigation

### Basic TabView

```swift
struct MainTabView: View {
    @State private var selectedTab = 0

    var body: some View {
        TabView(selection: $selectedTab) {
            HomeView()
                .tabItem {
                    Label("Home", systemImage: "house")
                }
                .tag(0)

            SearchView()
                .tabItem {
                    Label("Search", systemImage: "magnifyingglass")
                }
                .tag(1)

            ProfileView()
                .tabItem {
                    Label("Profile", systemImage: "person")
                }
                .tag(2)
                .badge(unreadCount)
        }
    }
}
```

### Tab with Custom Badge

```swift
struct BadgedTabView: View {
    @State private var selectedTab: Tab = .home
    @State private var cartCount = 3

    enum Tab: String, CaseIterable {
        case home, search, cart, profile

        var icon: String {
            switch self {
            case .home: return "house"
            case .search: return "magnifyingglass"
            case .cart: return "cart"
            case .profile: return "person"
            }
        }
    }

    var body: some View {
        TabView(selection: $selectedTab) {
            ForEach(Tab.allCases, id: \.self) { tab in
                NavigationStack {
                    contentView(for: tab)
                }
                .tabItem {
                    Label(tab.rawValue.capitalized, systemImage: tab.icon)
                }
                .tag(tab)
                .badge(tab == .cart ? cartCount : 0)
            }
        }
    }
}
```

## Deep Linking

### URL-Based Navigation

```swift
struct DeepLinkableApp: App {
    @StateObject private var router = NavigationRouter()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(router)
                .onOpenURL { url in
                    router.handle(url: url)
                }
        }
    }
}

class NavigationRouter: ObservableObject {
    @Published var path = NavigationPath()
    @Published var selectedTab: Tab = .home

    func handle(url: URL) {
        guard url.scheme == "myapp" else { return }

        switch url.host {
        case "item":
            if let id = Int(url.lastPathComponent) {
                selectedTab = .home
                path = NavigationPath()
                path.append(Destination.itemDetail(id: id))
            }
        case "settings":
            selectedTab = .profile
            path = NavigationPath()
            path.append(Destination.settings)
        default:
            break
        }
    }
}
```

### Universal Links

```swift
struct UniversalLinkHandler: View {
    @EnvironmentObject private var router: NavigationRouter

    var body: some View {
        ContentView()
            .onContinueUserActivity(NSUserActivityTypeBrowsingWeb) { activity in
                guard let url = activity.webpageURL else { return }
                handleUniversalLink(url)
            }
    }

    private func handleUniversalLink(_ url: URL) {
        // Parse URL path and navigate accordingly
        let pathComponents = url.pathComponents

        if pathComponents.contains("product"),
           let idString = pathComponents.last,
           let id = Int(idString) {
            router.navigate(to: .product(id: id))
        }
    }
}
```

## Navigation Coordinator Pattern

```swift
@MainActor
class NavigationCoordinator: ObservableObject {
    @Published var path = NavigationPath()
    @Published var sheet: Sheet?
    @Published var fullScreenCover: FullScreenCover?

    enum Sheet: Identifiable {
        case settings
        case newItem
        case editItem(Item)

        var id: String {
            switch self {
            case .settings: return "settings"
            case .newItem: return "newItem"
            case .editItem(let item): return "editItem-\(item.id)"
            }
        }
    }

    enum FullScreenCover: Identifiable {
        case onboarding
        case camera

        var id: String {
            switch self {
            case .onboarding: return "onboarding"
            case .camera: return "camera"
            }
        }
    }

    func push(_ destination: Destination) {
        path.append(destination)
    }

    func pop() {
        guard !path.isEmpty else { return }
        path.removeLast()
    }

    func popToRoot() {
        path = NavigationPath()
    }

    func present(_ sheet: Sheet) {
        self.sheet = sheet
    }

    func presentFullScreen(_ cover: FullScreenCover) {
        self.fullScreenCover = cover
    }

    func dismiss() {
        if fullScreenCover != nil {
            fullScreenCover = nil
        } else if sheet != nil {
            sheet = nil
        }
    }
}
```

## Navigation Transitions (iOS 18+)

### Custom Navigation Transitions

```swift
struct CustomTransitionView: View {
    @Namespace private var namespace

    var body: some View {
        NavigationStack {
            List(items) { item in
                NavigationLink(value: item) {
                    ItemRow(item: item)
                        .matchedTransitionSource(id: item.id, in: namespace)
                }
            }
            .navigationDestination(for: Item.self) { item in
                ItemDetailView(item: item)
                    .navigationTransition(.zoom(sourceID: item.id, in: namespace))
            }
        }
    }
}
```

### Hero Transitions

```swift
struct HeroTransitionView: View {
    @Namespace private var animation
    @State private var selectedItem: Item?

    var body: some View {
        ZStack {
            ScrollView {
                LazyVGrid(columns: columns) {
                    ForEach(items) { item in
                        if selectedItem?.id != item.id {
                            ItemCard(item: item)
                                .matchedGeometryEffect(id: item.id, in: animation)
                                .onTapGesture {
                                    withAnimation(.spring(response: 0.3)) {
                                        selectedItem = item
                                    }
                                }
                        }
                    }
                }
            }

            if let item = selectedItem {
                ItemDetailView(item: item)
                    .matchedGeometryEffect(id: item.id, in: animation)
                    .onTapGesture {
                        withAnimation(.spring(response: 0.3)) {
                            selectedItem = nil
                        }
                    }
            }
        }
    }
}
```
