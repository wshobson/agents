---
name: react-native-design
description: Master React Native styling, navigation, and Reanimated animations for cross-platform mobile development. Use when building React Native apps, implementing navigation patterns, or creating performant animations.
---

# React Native Design

Master React Native styling patterns, React Navigation, and Reanimated 3 to build performant, cross-platform mobile applications with native-quality user experiences.

## When to Use This Skill

- Building cross-platform mobile apps with React Native
- Implementing navigation with React Navigation 6+
- Creating performant animations with Reanimated 3
- Styling components with StyleSheet and styled-components
- Building responsive layouts for different screen sizes
- Implementing platform-specific designs (iOS/Android)
- Creating gesture-driven interactions with Gesture Handler
- Optimizing React Native performance

## Core Concepts

### 1. StyleSheet and Styling

**Basic StyleSheet:**

```typescript
import { StyleSheet, View, Text } from 'react-native';

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
    backgroundColor: '#ffffff',
  },
  title: {
    fontSize: 24,
    fontWeight: '600',
    color: '#1a1a1a',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: '#666666',
    lineHeight: 24,
  },
});

function Card() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Title</Text>
      <Text style={styles.subtitle}>Subtitle text</Text>
    </View>
  );
}
```

**Dynamic Styles:**

```typescript
interface CardProps {
  variant: 'primary' | 'secondary';
  disabled?: boolean;
}

function Card({ variant, disabled }: CardProps) {
  return (
    <View style={[
      styles.card,
      variant === 'primary' ? styles.primary : styles.secondary,
      disabled && styles.disabled,
    ]}>
      <Text style={styles.text}>Content</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    padding: 16,
    borderRadius: 12,
  },
  primary: {
    backgroundColor: '#6366f1',
  },
  secondary: {
    backgroundColor: '#f3f4f6',
    borderWidth: 1,
    borderColor: '#e5e7eb',
  },
  disabled: {
    opacity: 0.5,
  },
  text: {
    fontSize: 16,
  },
});
```

### 2. Flexbox Layout

**Row and Column Layouts:**

```typescript
const styles = StyleSheet.create({
  // Vertical stack (column)
  column: {
    flexDirection: "column",
    gap: 12,
  },
  // Horizontal stack (row)
  row: {
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
  },
  // Space between items
  spaceBetween: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },
  // Centered content
  centered: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },
  // Fill remaining space
  fill: {
    flex: 1,
  },
});
```

### 3. React Navigation Setup

**Stack Navigator:**

```typescript
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

type RootStackParamList = {
  Home: undefined;
  Detail: { itemId: string };
  Settings: undefined;
};

const Stack = createNativeStackNavigator<RootStackParamList>();

function AppNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator
        initialRouteName="Home"
        screenOptions={{
          headerStyle: { backgroundColor: '#6366f1' },
          headerTintColor: '#ffffff',
          headerTitleStyle: { fontWeight: '600' },
        }}
      >
        <Stack.Screen
          name="Home"
          component={HomeScreen}
          options={{ title: 'Home' }}
        />
        <Stack.Screen
          name="Detail"
          component={DetailScreen}
          options={({ route }) => ({
            title: `Item ${route.params.itemId}`,
          })}
        />
        <Stack.Screen name="Settings" component={SettingsScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
```

**Tab Navigator:**

```typescript
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Ionicons } from '@expo/vector-icons';

type TabParamList = {
  Home: undefined;
  Search: undefined;
  Profile: undefined;
};

const Tab = createBottomTabNavigator<TabParamList>();

function TabNavigator() {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused, color, size }) => {
          const icons: Record<string, keyof typeof Ionicons.glyphMap> = {
            Home: focused ? 'home' : 'home-outline',
            Search: focused ? 'search' : 'search-outline',
            Profile: focused ? 'person' : 'person-outline',
          };
          return <Ionicons name={icons[route.name]} size={size} color={color} />;
        },
        tabBarActiveTintColor: '#6366f1',
        tabBarInactiveTintColor: '#9ca3af',
      })}
    >
      <Tab.Screen name="Home" component={HomeScreen} />
      <Tab.Screen name="Search" component={SearchScreen} />
      <Tab.Screen name="Profile" component={ProfileScreen} />
    </Tab.Navigator>
  );
}
```

### 4. Reanimated 3 Basics

**Animated Values:**

```typescript
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withSpring,
  withTiming,
} from 'react-native-reanimated';

function AnimatedBox() {
  const scale = useSharedValue(1);
  const opacity = useSharedValue(1);

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
    opacity: opacity.value,
  }));

  const handlePress = () => {
    scale.value = withSpring(1.2, {}, () => {
      scale.value = withSpring(1);
    });
  };

  return (
    <Pressable onPress={handlePress}>
      <Animated.View style={[styles.box, animatedStyle]} />
    </Pressable>
  );
}
```

**Gesture Handler Integration:**

```typescript
import { Gesture, GestureDetector } from 'react-native-gesture-handler';
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withSpring,
} from 'react-native-reanimated';

function DraggableCard() {
  const translateX = useSharedValue(0);
  const translateY = useSharedValue(0);

  const gesture = Gesture.Pan()
    .onUpdate((event) => {
      translateX.value = event.translationX;
      translateY.value = event.translationY;
    })
    .onEnd(() => {
      translateX.value = withSpring(0);
      translateY.value = withSpring(0);
    });

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [
      { translateX: translateX.value },
      { translateY: translateY.value },
    ],
  }));

  return (
    <GestureDetector gesture={gesture}>
      <Animated.View style={[styles.card, animatedStyle]}>
        <Text>Drag me!</Text>
      </Animated.View>
    </GestureDetector>
  );
}
```

### 5. Platform-Specific Styling

```typescript
import { Platform, StyleSheet } from "react-native";

const styles = StyleSheet.create({
  container: {
    padding: 16,
    ...Platform.select({
      ios: {
        shadowColor: "#000",
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.1,
        shadowRadius: 4,
      },
      android: {
        elevation: 4,
      },
    }),
  },
  text: {
    fontFamily: Platform.OS === "ios" ? "SF Pro Text" : "Roboto",
    fontSize: 16,
  },
});

// Platform-specific components
import { Platform } from "react-native";
const StatusBarHeight = Platform.OS === "ios" ? 44 : 0;
```

## Quick Start Component

```typescript
import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  Pressable,
  Image,
} from 'react-native';
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withSpring,
} from 'react-native-reanimated';

interface ItemCardProps {
  title: string;
  subtitle: string;
  imageUrl: string;
  onPress: () => void;
}

const AnimatedPressable = Animated.createAnimatedComponent(Pressable);

export function ItemCard({ title, subtitle, imageUrl, onPress }: ItemCardProps) {
  const scale = useSharedValue(1);

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
  }));

  return (
    <AnimatedPressable
      style={[styles.card, animatedStyle]}
      onPress={onPress}
      onPressIn={() => { scale.value = withSpring(0.97); }}
      onPressOut={() => { scale.value = withSpring(1); }}
    >
      <Image source={{ uri: imageUrl }} style={styles.image} />
      <View style={styles.content}>
        <Text style={styles.title} numberOfLines={1}>
          {title}
        </Text>
        <Text style={styles.subtitle} numberOfLines={2}>
          {subtitle}
        </Text>
      </View>
    </AnimatedPressable>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: '#ffffff',
    borderRadius: 16,
    overflow: 'hidden',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 4,
  },
  image: {
    width: '100%',
    height: 160,
    backgroundColor: '#f3f4f6',
  },
  content: {
    padding: 16,
    gap: 4,
  },
  title: {
    fontSize: 18,
    fontWeight: '600',
    color: '#1f2937',
  },
  subtitle: {
    fontSize: 14,
    color: '#6b7280',
    lineHeight: 20,
  },
});
```

## Best Practices

1. **Use TypeScript**: Define navigation and prop types for type safety
2. **Memoize Components**: Use `React.memo` and `useCallback` to prevent unnecessary rerenders
3. **Run Animations on UI Thread**: Use Reanimated worklets for 60fps animations
4. **Avoid Inline Styles**: Use StyleSheet.create for performance
5. **Handle Safe Areas**: Use `SafeAreaView` or `useSafeAreaInsets`
6. **Test on Real Devices**: Simulator/emulator performance differs from real devices
7. **Use FlatList for Lists**: Never use ScrollView with map for long lists
8. **Platform-Specific Code**: Use Platform.select for iOS/Android differences

## Common Issues

- **Gesture Conflicts**: Wrap gestures with `GestureDetector` and use `simultaneousHandlers`
- **Navigation Type Errors**: Define `ParamList` types for all navigators
- **Animation Jank**: Move animations to UI thread with `runOnUI` worklets
- **Memory Leaks**: Cancel animations and cleanup in useEffect
- **Font Loading**: Use `expo-font` or `react-native-asset` for custom fonts
- **Safe Area Issues**: Test on notched devices (iPhone, Android with cutouts)

## Resources

- [React Native Documentation](https://reactnative.dev/)
- [React Navigation](https://reactnavigation.org/)
- [Reanimated Documentation](https://docs.swmansion.com/react-native-reanimated/)
- [Gesture Handler](https://docs.swmansion.com/react-native-gesture-handler/)
- [Expo Documentation](https://docs.expo.dev/)
