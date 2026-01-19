# SwiftUI Component Library

## Lists and Collections

### Basic List

```swift
struct ItemListView: View {
    @State private var items: [Item] = []

    var body: some View {
        List {
            ForEach(items) { item in
                ItemRow(item: item)
            }
            .onDelete(perform: deleteItems)
            .onMove(perform: moveItems)
        }
        .listStyle(.insetGrouped)
        .refreshable {
            await loadItems()
        }
    }

    private func deleteItems(at offsets: IndexSet) {
        items.remove(atOffsets: offsets)
    }

    private func moveItems(from source: IndexSet, to destination: Int) {
        items.move(fromOffsets: source, toOffset: destination)
    }
}
```

### Sectioned List

```swift
struct SectionedListView: View {
    let groupedItems: [String: [Item]]

    var body: some View {
        List {
            ForEach(groupedItems.keys.sorted(), id: \.self) { key in
                Section(header: Text(key)) {
                    ForEach(groupedItems[key] ?? []) { item in
                        ItemRow(item: item)
                    }
                }
            }
        }
        .listStyle(.sidebar)
    }
}
```

### Search Integration

```swift
struct SearchableListView: View {
    @State private var searchText = ""
    @State private var items: [Item] = []

    var filteredItems: [Item] {
        if searchText.isEmpty {
            return items
        }
        return items.filter { $0.name.localizedCaseInsensitiveContains(searchText) }
    }

    var body: some View {
        NavigationStack {
            List(filteredItems) { item in
                ItemRow(item: item)
            }
            .searchable(text: $searchText, prompt: "Search items")
            .searchSuggestions {
                ForEach(searchSuggestions, id: \.self) { suggestion in
                    Text(suggestion)
                        .searchCompletion(suggestion)
                }
            }
            .navigationTitle("Items")
        }
    }
}
```

## Forms and Input

### Settings Form

```swift
struct SettingsView: View {
    @AppStorage("notifications") private var notificationsEnabled = true
    @AppStorage("soundEnabled") private var soundEnabled = true
    @State private var selectedTheme = Theme.system
    @State private var username = ""

    var body: some View {
        Form {
            Section("Account") {
                TextField("Username", text: $username)
                    .textContentType(.username)
                    .autocorrectionDisabled()
            }

            Section("Preferences") {
                Toggle("Enable Notifications", isOn: $notificationsEnabled)
                Toggle("Sound Effects", isOn: $soundEnabled)

                Picker("Theme", selection: $selectedTheme) {
                    ForEach(Theme.allCases) { theme in
                        Text(theme.rawValue).tag(theme)
                    }
                }
            }

            Section("About") {
                LabeledContent("Version", value: "1.0.0")

                Link(destination: URL(string: "https://example.com/privacy")!) {
                    Text("Privacy Policy")
                }
            }
        }
        .navigationTitle("Settings")
    }
}
```

### Custom Input Fields

```swift
struct ValidatedTextField: View {
    let title: String
    @Binding var text: String
    let validation: (String) -> Bool

    @State private var isValid = true
    @FocusState private var isFocused: Bool

    var body: some View {
        VStack(alignment: .leading, spacing: 4) {
            Text(title)
                .font(.caption)
                .foregroundStyle(.secondary)

            TextField(title, text: $text)
                .textFieldStyle(.roundedBorder)
                .focused($isFocused)
                .overlay(
                    RoundedRectangle(cornerRadius: 8)
                        .stroke(borderColor, lineWidth: 1)
                )
                .onChange(of: text) { _, newValue in
                    isValid = validation(newValue)
                }

            if !isValid && !text.isEmpty {
                Text("Invalid input")
                    .font(.caption)
                    .foregroundStyle(.red)
            }
        }
    }

    private var borderColor: Color {
        if isFocused {
            return isValid ? .blue : .red
        }
        return .clear
    }
}
```

## Buttons and Actions

### Button Styles

```swift
// Primary filled button
Button("Continue") {
    // action
}
.buttonStyle(.borderedProminent)
.controlSize(.large)

// Secondary button
Button("Cancel") {
    // action
}
.buttonStyle(.bordered)

// Destructive button
Button("Delete", role: .destructive) {
    // action
}
.buttonStyle(.bordered)

// Custom button style
struct ScaleButtonStyle: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .scaleEffect(configuration.isPressed ? 0.95 : 1.0)
            .animation(.easeInOut(duration: 0.1), value: configuration.isPressed)
    }
}
```

### Menu and Context Menu

```swift
// Menu button
Menu {
    Button("Edit", systemImage: "pencil") { }
    Button("Duplicate", systemImage: "doc.on.doc") { }
    Divider()
    Button("Delete", systemImage: "trash", role: .destructive) { }
} label: {
    Image(systemName: "ellipsis.circle")
}

// Context menu on any view
Text("Long press me")
    .contextMenu {
        Button("Copy", systemImage: "doc.on.doc") { }
        Button("Share", systemImage: "square.and.arrow.up") { }
    } preview: {
        ItemPreviewView()
    }
```

## Sheets and Modals

### Sheet Presentation

```swift
struct ParentView: View {
    @State private var showSettings = false
    @State private var selectedItem: Item?

    var body: some View {
        VStack {
            Button("Settings") {
                showSettings = true
            }
        }
        .sheet(isPresented: $showSettings) {
            SettingsSheet()
                .presentationDetents([.medium, .large])
                .presentationDragIndicator(.visible)
        }
        .sheet(item: $selectedItem) { item in
            ItemDetailSheet(item: item)
                .presentationDetents([.height(300), .large])
                .presentationCornerRadius(24)
        }
    }
}

struct SettingsSheet: View {
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        NavigationStack {
            SettingsContent()
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

### Confirmation Dialog

```swift
struct DeleteConfirmationView: View {
    @State private var showConfirmation = false

    var body: some View {
        Button("Delete Account", role: .destructive) {
            showConfirmation = true
        }
        .confirmationDialog(
            "Delete Account",
            isPresented: $showConfirmation,
            titleVisibility: .visible
        ) {
            Button("Delete", role: .destructive) {
                deleteAccount()
            }
            Button("Cancel", role: .cancel) { }
        } message: {
            Text("This action cannot be undone.")
        }
    }
}
```

## Loading and Progress

### Progress Indicators

```swift
// Indeterminate spinner
ProgressView()
    .progressViewStyle(.circular)

// Determinate progress
ProgressView(value: downloadProgress, total: 1.0) {
    Text("Downloading...")
} currentValueLabel: {
    Text("\(Int(downloadProgress * 100))%")
}

// Custom loading view
struct LoadingOverlay: View {
    let message: String

    var body: some View {
        ZStack {
            Color.black.opacity(0.4)
                .ignoresSafeArea()

            VStack(spacing: 16) {
                ProgressView()
                    .scaleEffect(1.5)
                    .tint(.white)

                Text(message)
                    .font(.subheadline)
                    .foregroundStyle(.white)
            }
            .padding(24)
            .background(.ultraThinMaterial, in: RoundedRectangle(cornerRadius: 16))
        }
    }
}
```

### Skeleton Loading

```swift
struct SkeletonRow: View {
    @State private var isAnimating = false

    var body: some View {
        HStack(spacing: 12) {
            Circle()
                .fill(.gray.opacity(0.3))
                .frame(width: 44, height: 44)

            VStack(alignment: .leading, spacing: 8) {
                RoundedRectangle(cornerRadius: 4)
                    .fill(.gray.opacity(0.3))
                    .frame(height: 14)
                    .frame(maxWidth: 200)

                RoundedRectangle(cornerRadius: 4)
                    .fill(.gray.opacity(0.2))
                    .frame(height: 12)
                    .frame(maxWidth: 150)
            }
        }
        .opacity(isAnimating ? 0.5 : 1.0)
        .animation(.easeInOut(duration: 0.8).repeatForever(), value: isAnimating)
        .onAppear { isAnimating = true }
    }
}
```

## Async Content Loading

### AsyncImage

```swift
AsyncImage(url: imageURL) { phase in
    switch phase {
    case .empty:
        ProgressView()
    case .success(let image):
        image
            .resizable()
            .aspectRatio(contentMode: .fill)
    case .failure:
        Image(systemName: "photo")
            .foregroundStyle(.secondary)
    @unknown default:
        EmptyView()
    }
}
.frame(width: 100, height: 100)
.clipShape(RoundedRectangle(cornerRadius: 8))
```

### Task-Based Loading

```swift
struct AsyncContentView: View {
    @State private var items: [Item] = []
    @State private var isLoading = true
    @State private var error: Error?

    var body: some View {
        Group {
            if isLoading {
                ProgressView("Loading...")
            } else if let error {
                ContentUnavailableView(
                    "Failed to Load",
                    systemImage: "exclamationmark.triangle",
                    description: Text(error.localizedDescription)
                )
            } else if items.isEmpty {
                ContentUnavailableView(
                    "No Items",
                    systemImage: "tray",
                    description: Text("Add your first item to get started.")
                )
            } else {
                List(items) { item in
                    ItemRow(item: item)
                }
            }
        }
        .task {
            await loadItems()
        }
    }

    private func loadItems() async {
        do {
            items = try await api.fetchItems()
            isLoading = false
        } catch {
            self.error = error
            isLoading = false
        }
    }
}
```

## Animations

### Implicit Animations

```swift
struct AnimatedCard: View {
    @State private var isExpanded = false

    var body: some View {
        VStack {
            Text("Tap to expand")

            if isExpanded {
                Text("Additional content here")
                    .transition(.move(edge: .top).combined(with: .opacity))
            }
        }
        .padding()
        .frame(maxWidth: .infinity)
        .background(.blue.opacity(0.1), in: RoundedRectangle(cornerRadius: 12))
        .onTapGesture {
            withAnimation(.spring(response: 0.3, dampingFraction: 0.7)) {
                isExpanded.toggle()
            }
        }
    }
}
```

### Custom Transitions

```swift
extension AnyTransition {
    static var slideAndFade: AnyTransition {
        .asymmetric(
            insertion: .move(edge: .trailing).combined(with: .opacity),
            removal: .move(edge: .leading).combined(with: .opacity)
        )
    }

    static var scaleAndFade: AnyTransition {
        .scale(scale: 0.8).combined(with: .opacity)
    }
}
```

### Phase Animator (iOS 17+)

```swift
struct PulsingButton: View {
    var body: some View {
        Button("Tap Me") { }
            .buttonStyle(.borderedProminent)
            .phaseAnimator([false, true]) { content, phase in
                content
                    .scaleEffect(phase ? 1.05 : 1.0)
            } animation: { _ in
                .easeInOut(duration: 0.5)
            }
    }
}
```

## Gestures

### Drag Gesture

```swift
struct DraggableCard: View {
    @State private var offset = CGSize.zero
    @State private var isDragging = false

    var body: some View {
        RoundedRectangle(cornerRadius: 16)
            .fill(.blue)
            .frame(width: 200, height: 150)
            .offset(offset)
            .scaleEffect(isDragging ? 1.05 : 1.0)
            .gesture(
                DragGesture()
                    .onChanged { value in
                        offset = value.translation
                        isDragging = true
                    }
                    .onEnded { _ in
                        withAnimation(.spring()) {
                            offset = .zero
                            isDragging = false
                        }
                    }
            )
    }
}
```

### Simultaneous Gestures

```swift
struct ZoomableImage: View {
    @State private var scale: CGFloat = 1.0
    @State private var lastScale: CGFloat = 1.0

    var body: some View {
        Image("photo")
            .resizable()
            .aspectRatio(contentMode: .fit)
            .scaleEffect(scale)
            .gesture(
                MagnificationGesture()
                    .onChanged { value in
                        scale = lastScale * value
                    }
                    .onEnded { _ in
                        lastScale = scale
                    }
            )
            .gesture(
                TapGesture(count: 2)
                    .onEnded {
                        withAnimation {
                            scale = 1.0
                            lastScale = 1.0
                        }
                    }
            )
    }
}
```
