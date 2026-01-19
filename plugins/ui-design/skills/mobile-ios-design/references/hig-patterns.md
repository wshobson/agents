# iOS Human Interface Guidelines Patterns

## Layout and Spacing

### Standard Margins and Padding

```swift
// System standard margins
private let standardMargin: CGFloat = 16
private let compactMargin: CGFloat = 8
private let largeMargin: CGFloat = 24

// Content insets following HIG
extension EdgeInsets {
    static let standard = EdgeInsets(top: 16, leading: 16, bottom: 16, trailing: 16)
    static let listRow = EdgeInsets(top: 12, leading: 16, bottom: 12, trailing: 16)
    static let card = EdgeInsets(top: 16, leading: 16, bottom: 16, trailing: 16)
}
```

### Safe Area Handling

```swift
struct SafeAreaAwareView: View {
    var body: some View {
        ScrollView {
            LazyVStack(spacing: 16) {
                ForEach(items) { item in
                    ItemRow(item: item)
                }
            }
            .padding(.horizontal)
        }
        .safeAreaInset(edge: .bottom) {
            // Floating action area
            HStack {
                Button("Cancel") { }
                    .buttonStyle(.bordered)
                Spacer()
                Button("Confirm") { }
                    .buttonStyle(.borderedProminent)
            }
            .padding()
            .background(.regularMaterial)
        }
    }
}
```

### Adaptive Layouts

```swift
struct AdaptiveGridView: View {
    @Environment(\.horizontalSizeClass) private var sizeClass

    private var columns: [GridItem] {
        switch sizeClass {
        case .compact:
            return [GridItem(.flexible())]
        case .regular:
            return [
                GridItem(.flexible()),
                GridItem(.flexible()),
                GridItem(.flexible())
            ]
        default:
            return [GridItem(.flexible())]
        }
    }

    var body: some View {
        ScrollView {
            LazyVGrid(columns: columns, spacing: 16) {
                ForEach(items) { item in
                    ItemCard(item: item)
                }
            }
            .padding()
        }
    }
}
```

## Typography Hierarchy

### System Font Styles

```swift
// HIG-compliant typography scale
struct Typography {
    // Titles
    static let largeTitle = Font.largeTitle.weight(.bold)      // 34pt bold
    static let title = Font.title.weight(.semibold)            // 28pt semibold
    static let title2 = Font.title2.weight(.semibold)          // 22pt semibold
    static let title3 = Font.title3.weight(.semibold)          // 20pt semibold

    // Headlines and body
    static let headline = Font.headline                         // 17pt semibold
    static let body = Font.body                                 // 17pt regular
    static let callout = Font.callout                          // 16pt regular

    // Supporting text
    static let subheadline = Font.subheadline                  // 15pt regular
    static let footnote = Font.footnote                        // 13pt regular
    static let caption = Font.caption                          // 12pt regular
    static let caption2 = Font.caption2                        // 11pt regular
}
```

### Custom Font with Dynamic Type

```swift
extension Font {
    static func customBody(_ name: String) -> Font {
        .custom(name, size: 17, relativeTo: .body)
    }

    static func customHeadline(_ name: String) -> Font {
        .custom(name, size: 17, relativeTo: .headline)
            .weight(.semibold)
    }
}

// Usage
Text("Custom styled text")
    .font(.customBody("Avenir Next"))
```

## Color System

### Semantic Colors

```swift
// Use semantic colors for automatic light/dark mode support
extension Color {
    // Labels
    static let primaryLabel = Color.primary
    static let secondaryLabel = Color.secondary
    static let tertiaryLabel = Color(uiColor: .tertiaryLabel)

    // Backgrounds
    static let systemBackground = Color(uiColor: .systemBackground)
    static let secondaryBackground = Color(uiColor: .secondarySystemBackground)
    static let groupedBackground = Color(uiColor: .systemGroupedBackground)

    // Fills
    static let primaryFill = Color(uiColor: .systemFill)
    static let secondaryFill = Color(uiColor: .secondarySystemFill)

    // Separators
    static let separator = Color(uiColor: .separator)
    static let opaqueSeparator = Color(uiColor: .opaqueSeparator)
}
```

### Tint Colors

```swift
// App-wide tint color
struct AppColors {
    static let primary = Color.blue
    static let secondary = Color.purple
    static let success = Color.green
    static let warning = Color.orange
    static let error = Color.red

    // Semantic tints
    static let interactive = Color.accentColor
    static let destructive = Color.red
}

// Apply tint to views
ContentView()
    .tint(AppColors.primary)
```

## Navigation Patterns

### Hierarchical Navigation

```swift
struct MasterDetailView: View {
    @State private var selectedItem: Item?
    @Environment(\.horizontalSizeClass) private var sizeClass

    var body: some View {
        NavigationSplitView {
            // Sidebar
            List(items, selection: $selectedItem) { item in
                NavigationLink(value: item) {
                    ItemRow(item: item)
                }
            }
            .navigationTitle("Items")
            .toolbar {
                ToolbarItem(placement: .primaryAction) {
                    Button("Add", systemImage: "plus") { }
                }
            }
        } detail: {
            // Detail view
            if let item = selectedItem {
                ItemDetailView(item: item)
            } else {
                ContentUnavailableView(
                    "Select an Item",
                    systemImage: "sidebar.leading"
                )
            }
        }
        .navigationSplitViewStyle(.balanced)
    }
}
```

### Tab-Based Navigation

```swift
struct MainTabView: View {
    @State private var selectedTab: Tab = .home

    enum Tab: String, CaseIterable {
        case home, explore, notifications, profile

        var title: String {
            rawValue.capitalized
        }

        var systemImage: String {
            switch self {
            case .home: return "house"
            case .explore: return "magnifyingglass"
            case .notifications: return "bell"
            case .profile: return "person"
            }
        }
    }

    var body: some View {
        TabView(selection: $selectedTab) {
            ForEach(Tab.allCases, id: \.self) { tab in
                NavigationStack {
                    tabContent(for: tab)
                }
                .tabItem {
                    Label(tab.title, systemImage: tab.systemImage)
                }
                .tag(tab)
            }
        }
    }

    @ViewBuilder
    private func tabContent(for tab: Tab) -> some View {
        switch tab {
        case .home:
            HomeView()
        case .explore:
            ExploreView()
        case .notifications:
            NotificationsView()
        case .profile:
            ProfileView()
        }
    }
}
```

## Toolbar Patterns

### Standard Toolbar Items

```swift
struct ContentView: View {
    @State private var isEditing = false

    var body: some View {
        NavigationStack {
            List { /* content */ }
            .navigationTitle("Items")
            .toolbar {
                // Leading items
                ToolbarItem(placement: .topBarLeading) {
                    EditButton()
                }

                // Trailing items
                ToolbarItemGroup(placement: .topBarTrailing) {
                    Button("Filter", systemImage: "line.3.horizontal.decrease.circle") { }
                    Button("Add", systemImage: "plus") { }
                }

                // Bottom bar
                ToolbarItemGroup(placement: .bottomBar) {
                    Button("Archive", systemImage: "archivebox") { }
                    Spacer()
                    Text("\(itemCount) items")
                        .font(.footnote)
                        .foregroundStyle(.secondary)
                    Spacer()
                    Button("Share", systemImage: "square.and.arrow.up") { }
                }
            }
            .toolbarBackground(.visible, for: .bottomBar)
        }
    }
}
```

### Search Integration

```swift
struct SearchableView: View {
    @State private var searchText = ""
    @State private var searchScope: SearchScope = .all
    @State private var isSearching = false

    enum SearchScope: String, CaseIterable {
        case all, titles, content
    }

    var body: some View {
        NavigationStack {
            List(filteredItems) { item in
                ItemRow(item: item)
            }
            .navigationTitle("Library")
            .searchable(
                text: $searchText,
                isPresented: $isSearching,
                placement: .navigationBarDrawer(displayMode: .always)
            )
            .searchScopes($searchScope) {
                ForEach(SearchScope.allCases, id: \.self) { scope in
                    Text(scope.rawValue.capitalized).tag(scope)
                }
            }
        }
    }
}
```

## Feedback Patterns

### Haptic Feedback

```swift
struct HapticFeedback {
    static func impact(_ style: UIImpactFeedbackGenerator.FeedbackStyle = .medium) {
        let generator = UIImpactFeedbackGenerator(style: style)
        generator.impactOccurred()
    }

    static func notification(_ type: UINotificationFeedbackGenerator.FeedbackType) {
        let generator = UINotificationFeedbackGenerator()
        generator.notificationOccurred(type)
    }

    static func selection() {
        let generator = UISelectionFeedbackGenerator()
        generator.selectionChanged()
    }
}

// Usage
Button("Submit") {
    HapticFeedback.notification(.success)
    submit()
}
```

### Visual Feedback

```swift
struct FeedbackButton: View {
    let title: String
    let action: () -> Void

    @State private var showSuccess = false

    var body: some View {
        Button(title) {
            action()
            withAnimation {
                showSuccess = true
            }
            DispatchQueue.main.asyncAfter(deadline: .now() + 1.5) {
                withAnimation {
                    showSuccess = false
                }
            }
        }
        .overlay(alignment: .trailing) {
            if showSuccess {
                Image(systemName: "checkmark.circle.fill")
                    .foregroundStyle(.green)
                    .transition(.scale.combined(with: .opacity))
            }
        }
    }
}
```

## Accessibility

### VoiceOver Support

```swift
struct AccessibleCard: View {
    let item: Item

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text(item.title)
                .font(.headline)
            Text(item.subtitle)
                .font(.subheadline)
                .foregroundStyle(.secondary)

            HStack {
                Image(systemName: "star.fill")
                Text("\(item.rating, specifier: "%.1f")")
            }
        }
        .padding()
        .accessibilityElement(children: .combine)
        .accessibilityLabel("\(item.title), \(item.subtitle)")
        .accessibilityValue("Rating: \(item.rating) stars")
        .accessibilityHint("Double tap to view details")
        .accessibilityAddTraits(.isButton)
    }
}
```

### Dynamic Type Support

```swift
struct DynamicTypeView: View {
    @Environment(\.dynamicTypeSize) private var dynamicTypeSize

    var body: some View {
        Group {
            if dynamicTypeSize.isAccessibilitySize {
                // Stack vertically for accessibility sizes
                VStack(alignment: .leading, spacing: 12) {
                    leadingContent
                    trailingContent
                }
            } else {
                // Side-by-side for standard sizes
                HStack {
                    leadingContent
                    Spacer()
                    trailingContent
                }
            }
        }
    }

    var leadingContent: some View {
        Label("Items", systemImage: "folder")
    }

    var trailingContent: some View {
        Text("12")
            .foregroundStyle(.secondary)
    }
}
```

## Error Handling UI

### Error States

```swift
struct ErrorView: View {
    let error: Error
    let retryAction: () async -> Void

    var body: some View {
        ContentUnavailableView {
            Label("Unable to Load", systemImage: "exclamationmark.triangle")
        } description: {
            Text(error.localizedDescription)
        } actions: {
            Button("Try Again") {
                Task {
                    await retryAction()
                }
            }
            .buttonStyle(.borderedProminent)
        }
    }
}
```

### Empty States

```swift
struct EmptyStateView: View {
    let title: String
    let description: String
    let systemImage: String
    let action: (() -> Void)?
    let actionTitle: String?

    var body: some View {
        ContentUnavailableView {
            Label(title, systemImage: systemImage)
        } description: {
            Text(description)
        } actions: {
            if let action, let actionTitle {
                Button(actionTitle, action: action)
                    .buttonStyle(.borderedProminent)
            }
        }
    }
}

// Usage
EmptyStateView(
    title: "No Photos",
    description: "Take your first photo to get started.",
    systemImage: "camera",
    action: { showCamera = true },
    actionTitle: "Take Photo"
)
```
