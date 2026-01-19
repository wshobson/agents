---
name: mobile-ios-design
description: Master iOS Human Interface Guidelines and SwiftUI patterns for building native iOS apps. Use when designing iOS interfaces, implementing SwiftUI views, or ensuring apps follow Apple's design principles.
---

# iOS Mobile Design

Master iOS Human Interface Guidelines (HIG) and SwiftUI patterns to build polished, native iOS applications that feel at home on Apple platforms.

## When to Use This Skill

- Designing iOS app interfaces following Apple HIG
- Building SwiftUI views and layouts
- Implementing iOS navigation patterns (NavigationStack, TabView, sheets)
- Creating adaptive layouts for iPhone and iPad
- Using SF Symbols and system typography
- Building accessible iOS interfaces
- Implementing iOS-specific gestures and interactions
- Designing for Dynamic Type and Dark Mode

## Core Concepts

### 1. Human Interface Guidelines Principles

**Clarity**: Content is legible, icons are precise, adornments are subtle
**Deference**: UI helps users understand content without competing with it
**Depth**: Visual layers and motion convey hierarchy and enable navigation

**Platform Considerations:**

- **iOS**: Touch-first, compact displays, portrait orientation
- **iPadOS**: Larger canvas, multitasking, pointer support
- **visionOS**: Spatial computing, eye/hand input

### 2. SwiftUI Layout System

**Stack-Based Layouts:**

```swift
// Vertical stack with alignment
VStack(alignment: .leading, spacing: 12) {
    Text("Title")
        .font(.headline)
    Text("Subtitle")
        .font(.subheadline)
        .foregroundStyle(.secondary)
}

// Horizontal stack with flexible spacing
HStack {
    Image(systemName: "star.fill")
    Text("Featured")
    Spacer()
    Text("View All")
        .foregroundStyle(.blue)
}
```

**Grid Layouts:**

```swift
// Adaptive grid that fills available width
LazyVGrid(columns: [
    GridItem(.adaptive(minimum: 150, maximum: 200))
], spacing: 16) {
    ForEach(items) { item in
        ItemCard(item: item)
    }
}

// Fixed column grid
LazyVGrid(columns: [
    GridItem(.flexible()),
    GridItem(.flexible()),
    GridItem(.flexible())
], spacing: 12) {
    ForEach(items) { item in
        ItemThumbnail(item: item)
    }
}
```

### 3. Navigation Patterns

**NavigationStack (iOS 16+):**

```swift
struct ContentView: View {
    @State private var path = NavigationPath()

    var body: some View {
        NavigationStack(path: $path) {
            List(items) { item in
                NavigationLink(value: item) {
                    ItemRow(item: item)
                }
            }
            .navigationTitle("Items")
            .navigationDestination(for: Item.self) { item in
                ItemDetailView(item: item)
            }
        }
    }
}
```

**TabView:**

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
        }
    }
}
```

### 4. System Integration

**SF Symbols:**

```swift
// Basic symbol
Image(systemName: "heart.fill")
    .foregroundStyle(.red)

// Symbol with rendering mode
Image(systemName: "cloud.sun.fill")
    .symbolRenderingMode(.multicolor)

// Variable symbol (iOS 16+)
Image(systemName: "speaker.wave.3.fill", variableValue: volume)

// Symbol effect (iOS 17+)
Image(systemName: "bell.fill")
    .symbolEffect(.bounce, value: notificationCount)
```

**Dynamic Type:**

```swift
// Use semantic fonts
Text("Headline")
    .font(.headline)

Text("Body text that scales with user preferences")
    .font(.body)

// Custom font that respects Dynamic Type
Text("Custom")
    .font(.custom("Avenir", size: 17, relativeTo: .body))
```

### 5. Visual Design

**Colors and Materials:**

```swift
// Semantic colors that adapt to light/dark mode
Text("Primary")
    .foregroundStyle(.primary)
Text("Secondary")
    .foregroundStyle(.secondary)

// System materials for blur effects
Rectangle()
    .fill(.ultraThinMaterial)
    .frame(height: 100)

// Vibrant materials for overlays
Text("Overlay")
    .padding()
    .background(.regularMaterial, in: RoundedRectangle(cornerRadius: 12))
```

**Shadows and Depth:**

```swift
// Standard card shadow
RoundedRectangle(cornerRadius: 16)
    .fill(.background)
    .shadow(color: .black.opacity(0.1), radius: 8, y: 4)

// Elevated appearance
.shadow(radius: 2, y: 1)
.shadow(radius: 8, y: 4)
```

## Quick Start Component

```swift
import SwiftUI

struct FeatureCard: View {
    let title: String
    let description: String
    let systemImage: String

    var body: some View {
        HStack(spacing: 16) {
            Image(systemName: systemImage)
                .font(.title)
                .foregroundStyle(.blue)
                .frame(width: 44, height: 44)
                .background(.blue.opacity(0.1), in: Circle())

            VStack(alignment: .leading, spacing: 4) {
                Text(title)
                    .font(.headline)
                Text(description)
                    .font(.subheadline)
                    .foregroundStyle(.secondary)
                    .lineLimit(2)
            }

            Spacer()

            Image(systemName: "chevron.right")
                .foregroundStyle(.tertiary)
        }
        .padding()
        .background(.background, in: RoundedRectangle(cornerRadius: 12))
        .shadow(color: .black.opacity(0.05), radius: 4, y: 2)
    }
}
```

## Best Practices

1. **Use Semantic Colors**: Always use `.primary`, `.secondary`, `.background` for automatic light/dark mode support
2. **Embrace SF Symbols**: Use system symbols for consistency and automatic accessibility
3. **Support Dynamic Type**: Use semantic fonts (`.body`, `.headline`) instead of fixed sizes
4. **Add Accessibility**: Include `.accessibilityLabel()` and `.accessibilityHint()` modifiers
5. **Use Safe Areas**: Respect `safeAreaInset` and avoid hardcoded padding at screen edges
6. **Implement State Restoration**: Use `@SceneStorage` for preserving user state
7. **Support iPad Multitasking**: Design for split view and slide over
8. **Test on Device**: Simulator doesn't capture full haptic and performance experience

## Common Issues

- **Layout Breaking**: Use `.fixedSize()` sparingly; prefer flexible layouts
- **Performance Issues**: Use `LazyVStack`/`LazyHStack` for long scrolling lists
- **Navigation Bugs**: Ensure `NavigationLink` values are `Hashable`
- **Dark Mode Problems**: Avoid hardcoded colors; use semantic or asset catalog colors
- **Accessibility Failures**: Test with VoiceOver enabled
- **Memory Leaks**: Watch for strong reference cycles in closures

## Resources

- [Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)
- [SwiftUI Documentation](https://developer.apple.com/documentation/swiftui)
- [SF Symbols App](https://developer.apple.com/sf-symbols/)
- [WWDC SwiftUI Sessions](https://developer.apple.com/videos/swiftui/)
