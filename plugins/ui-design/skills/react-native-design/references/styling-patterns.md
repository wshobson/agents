# React Native Styling Patterns

## StyleSheet Fundamentals

### Creating Styles

```typescript
import { StyleSheet, ViewStyle, TextStyle, ImageStyle } from "react-native";

// Typed styles for better IDE support
interface Styles {
  container: ViewStyle;
  title: TextStyle;
  image: ImageStyle;
}

const styles = StyleSheet.create<Styles>({
  container: {
    flex: 1,
    padding: 16,
    backgroundColor: "#ffffff",
  },
  title: {
    fontSize: 24,
    fontWeight: "700",
    color: "#1f2937",
  },
  image: {
    width: 100,
    height: 100,
    borderRadius: 8,
  },
});
```

### Combining Styles

```typescript
import { StyleProp, ViewStyle } from 'react-native';

interface BoxProps {
  style?: StyleProp<ViewStyle>;
  variant?: 'default' | 'primary' | 'danger';
}

function Box({ style, variant = 'default' }: BoxProps) {
  return (
    <View
      style={[
        styles.base,
        variant === 'primary' && styles.primary,
        variant === 'danger' && styles.danger,
        style, // Allow external style overrides
      ]}
    />
  );
}

const styles = StyleSheet.create({
  base: {
    padding: 16,
    borderRadius: 8,
    backgroundColor: '#f3f4f6',
  },
  primary: {
    backgroundColor: '#6366f1',
  },
  danger: {
    backgroundColor: '#ef4444',
  },
});
```

## Theme System

### Theme Context

```typescript
import React, { createContext, useContext, useMemo } from 'react';
import { useColorScheme } from 'react-native';

interface Theme {
  colors: {
    primary: string;
    secondary: string;
    background: string;
    surface: string;
    text: string;
    textSecondary: string;
    border: string;
    error: string;
    success: string;
  };
  spacing: {
    xs: number;
    sm: number;
    md: number;
    lg: number;
    xl: number;
  };
  borderRadius: {
    sm: number;
    md: number;
    lg: number;
    full: number;
  };
  typography: {
    h1: { fontSize: number; fontWeight: string; lineHeight: number };
    h2: { fontSize: number; fontWeight: string; lineHeight: number };
    body: { fontSize: number; fontWeight: string; lineHeight: number };
    caption: { fontSize: number; fontWeight: string; lineHeight: number };
  };
}

const lightTheme: Theme = {
  colors: {
    primary: '#6366f1',
    secondary: '#8b5cf6',
    background: '#ffffff',
    surface: '#f9fafb',
    text: '#1f2937',
    textSecondary: '#6b7280',
    border: '#e5e7eb',
    error: '#ef4444',
    success: '#10b981',
  },
  spacing: {
    xs: 4,
    sm: 8,
    md: 16,
    lg: 24,
    xl: 32,
  },
  borderRadius: {
    sm: 4,
    md: 8,
    lg: 16,
    full: 9999,
  },
  typography: {
    h1: { fontSize: 32, fontWeight: '700', lineHeight: 40 },
    h2: { fontSize: 24, fontWeight: '600', lineHeight: 32 },
    body: { fontSize: 16, fontWeight: '400', lineHeight: 24 },
    caption: { fontSize: 12, fontWeight: '400', lineHeight: 16 },
  },
};

const darkTheme: Theme = {
  ...lightTheme,
  colors: {
    primary: '#818cf8',
    secondary: '#a78bfa',
    background: '#111827',
    surface: '#1f2937',
    text: '#f9fafb',
    textSecondary: '#9ca3af',
    border: '#374151',
    error: '#f87171',
    success: '#34d399',
  },
};

const ThemeContext = createContext<Theme>(lightTheme);

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const colorScheme = useColorScheme();
  const theme = useMemo(
    () => (colorScheme === 'dark' ? darkTheme : lightTheme),
    [colorScheme]
  );

  return (
    <ThemeContext.Provider value={theme}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  return useContext(ThemeContext);
}
```

### Using Theme

```typescript
import { useTheme } from './theme';

function ThemedCard() {
  const theme = useTheme();

  return (
    <View
      style={{
        backgroundColor: theme.colors.surface,
        padding: theme.spacing.md,
        borderRadius: theme.borderRadius.lg,
        borderWidth: 1,
        borderColor: theme.colors.border,
      }}
    >
      <Text
        style={{
          ...theme.typography.h2,
          color: theme.colors.text,
          marginBottom: theme.spacing.sm,
        }}
      >
        Card Title
      </Text>
      <Text
        style={{
          ...theme.typography.body,
          color: theme.colors.textSecondary,
        }}
      >
        Card description text
      </Text>
    </View>
  );
}
```

## Responsive Design

### Screen Dimensions

```typescript
import { Dimensions, useWindowDimensions, PixelRatio } from 'react-native';

// Get dimensions once (may be stale after rotation)
const { width: SCREEN_WIDTH, height: SCREEN_HEIGHT } = Dimensions.get('window');

// Responsive scaling
const guidelineBaseWidth = 375;
const guidelineBaseHeight = 812;

export const scale = (size: number) =>
  (SCREEN_WIDTH / guidelineBaseWidth) * size;

export const verticalScale = (size: number) =>
  (SCREEN_HEIGHT / guidelineBaseHeight) * size;

export const moderateScale = (size: number, factor = 0.5) =>
  size + (scale(size) - size) * factor;

// Hook for dynamic dimensions (handles rotation)
function ResponsiveComponent() {
  const { width, height } = useWindowDimensions();
  const isLandscape = width > height;
  const isTablet = width >= 768;

  return (
    <View style={{ flexDirection: isLandscape ? 'row' : 'column' }}>
      {/* Content */}
    </View>
  );
}
```

### Breakpoint System

```typescript
import { useWindowDimensions } from 'react-native';

type Breakpoint = 'sm' | 'md' | 'lg' | 'xl';

const breakpoints = {
  sm: 0,
  md: 768,
  lg: 1024,
  xl: 1280,
};

export function useBreakpoint(): Breakpoint {
  const { width } = useWindowDimensions();

  if (width >= breakpoints.xl) return 'xl';
  if (width >= breakpoints.lg) return 'lg';
  if (width >= breakpoints.md) return 'md';
  return 'sm';
}

export function useResponsiveValue<T>(values: Partial<Record<Breakpoint, T>>): T | undefined {
  const breakpoint = useBreakpoint();
  const breakpointOrder: Breakpoint[] = ['xl', 'lg', 'md', 'sm'];
  const currentIndex = breakpointOrder.indexOf(breakpoint);

  for (let i = currentIndex; i < breakpointOrder.length; i++) {
    const bp = breakpointOrder[i];
    if (values[bp] !== undefined) {
      return values[bp];
    }
  }

  return undefined;
}

// Usage
function ResponsiveGrid() {
  const columns = useResponsiveValue({ sm: 1, md: 2, lg: 3, xl: 4 }) ?? 1;

  return (
    <View style={{ flexDirection: 'row', flexWrap: 'wrap' }}>
      {items.map((item) => (
        <View key={item.id} style={{ width: `${100 / columns}%` }}>
          <ItemCard item={item} />
        </View>
      ))}
    </View>
  );
}
```

## Layout Components

### Container

```typescript
import { View, ViewStyle, StyleProp } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { useTheme } from './theme';

interface ContainerProps {
  children: React.ReactNode;
  style?: StyleProp<ViewStyle>;
  edges?: ('top' | 'bottom' | 'left' | 'right')[];
}

export function Container({ children, style, edges = ['top', 'bottom'] }: ContainerProps) {
  const insets = useSafeAreaInsets();
  const theme = useTheme();

  return (
    <View
      style={[
        {
          flex: 1,
          backgroundColor: theme.colors.background,
          paddingTop: edges.includes('top') ? insets.top : 0,
          paddingBottom: edges.includes('bottom') ? insets.bottom : 0,
          paddingLeft: edges.includes('left') ? insets.left : 0,
          paddingRight: edges.includes('right') ? insets.right : 0,
        },
        style,
      ]}
    >
      {children}
    </View>
  );
}
```

### Stack Components

```typescript
import { View, ViewStyle, StyleProp } from 'react-native';

interface StackProps {
  children: React.ReactNode;
  spacing?: number;
  style?: StyleProp<ViewStyle>;
}

export function VStack({ children, spacing = 8, style }: StackProps) {
  return (
    <View style={[{ gap: spacing }, style]}>
      {children}
    </View>
  );
}

export function HStack({ children, spacing = 8, style }: StackProps) {
  return (
    <View style={[{ flexDirection: 'row', alignItems: 'center', gap: spacing }, style]}>
      {children}
    </View>
  );
}

// Usage
function Example() {
  return (
    <VStack spacing={16}>
      <HStack spacing={8}>
        <Avatar />
        <VStack spacing={2}>
          <Text style={styles.name}>John Doe</Text>
          <Text style={styles.email}>john@example.com</Text>
        </VStack>
      </HStack>
      <Button title="Edit Profile" />
    </VStack>
  );
}
```

### Spacer

```typescript
import { View } from 'react-native';

interface SpacerProps {
  size?: number;
  flex?: number;
}

export function Spacer({ size, flex }: SpacerProps) {
  if (flex) {
    return <View style={{ flex }} />;
  }
  return <View style={{ height: size, width: size }} />;
}

// Usage
<HStack>
  <Text>Left</Text>
  <Spacer flex={1} />
  <Text>Right</Text>
</HStack>
```

## Shadow Styles

### Cross-Platform Shadows

```typescript
import { Platform, ViewStyle } from "react-native";

export function createShadow(elevation: number, color = "#000000"): ViewStyle {
  if (Platform.OS === "android") {
    return { elevation };
  }

  // iOS shadow mapping based on elevation
  const shadowMap: Record<number, ViewStyle> = {
    1: {
      shadowColor: color,
      shadowOffset: { width: 0, height: 1 },
      shadowOpacity: 0.18,
      shadowRadius: 1,
    },
    2: {
      shadowColor: color,
      shadowOffset: { width: 0, height: 2 },
      shadowOpacity: 0.2,
      shadowRadius: 2,
    },
    4: {
      shadowColor: color,
      shadowOffset: { width: 0, height: 2 },
      shadowOpacity: 0.22,
      shadowRadius: 4,
    },
    8: {
      shadowColor: color,
      shadowOffset: { width: 0, height: 4 },
      shadowOpacity: 0.25,
      shadowRadius: 8,
    },
    16: {
      shadowColor: color,
      shadowOffset: { width: 0, height: 8 },
      shadowOpacity: 0.3,
      shadowRadius: 16,
    },
  };

  return shadowMap[elevation] || shadowMap[4];
}

// Predefined shadow styles
export const shadows = {
  sm: createShadow(2),
  md: createShadow(4),
  lg: createShadow(8),
  xl: createShadow(16),
};

// Usage
const styles = StyleSheet.create({
  card: {
    backgroundColor: "#ffffff",
    borderRadius: 12,
    padding: 16,
    ...shadows.md,
  },
});
```

## Typography System

### Text Components

```typescript
import { Text as RNText, TextStyle, StyleProp, TextProps as RNTextProps } from 'react-native';
import { useTheme } from './theme';

type Variant = 'h1' | 'h2' | 'h3' | 'body' | 'bodySmall' | 'caption' | 'label';
type Color = 'primary' | 'secondary' | 'text' | 'textSecondary' | 'error' | 'success';

interface TextProps extends RNTextProps {
  variant?: Variant;
  color?: Color;
  weight?: 'normal' | 'medium' | 'semibold' | 'bold';
  align?: 'left' | 'center' | 'right';
}

const variantStyles: Record<Variant, TextStyle> = {
  h1: { fontSize: 32, lineHeight: 40, fontWeight: '700' },
  h2: { fontSize: 24, lineHeight: 32, fontWeight: '600' },
  h3: { fontSize: 20, lineHeight: 28, fontWeight: '600' },
  body: { fontSize: 16, lineHeight: 24, fontWeight: '400' },
  bodySmall: { fontSize: 14, lineHeight: 20, fontWeight: '400' },
  caption: { fontSize: 12, lineHeight: 16, fontWeight: '400' },
  label: { fontSize: 14, lineHeight: 20, fontWeight: '500' },
};

const weightStyles: Record<string, TextStyle> = {
  normal: { fontWeight: '400' },
  medium: { fontWeight: '500' },
  semibold: { fontWeight: '600' },
  bold: { fontWeight: '700' },
};

export function Text({
  variant = 'body',
  color = 'text',
  weight,
  align,
  style,
  ...props
}: TextProps) {
  const theme = useTheme();

  return (
    <RNText
      style={[
        variantStyles[variant],
        { color: theme.colors[color] },
        weight && weightStyles[weight],
        align && { textAlign: align },
        style,
      ]}
      {...props}
    />
  );
}

// Usage
<Text variant="h1">Heading</Text>
<Text variant="body" color="textSecondary">Body text</Text>
<Text variant="label" weight="semibold">Label</Text>
```

## Button Styles

### Customizable Button

```typescript
import { Pressable, StyleSheet, ActivityIndicator } from 'react-native';
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withSpring,
} from 'react-native-reanimated';
import { useTheme } from './theme';

type Variant = 'filled' | 'outlined' | 'ghost';
type Size = 'sm' | 'md' | 'lg';

interface ButtonProps {
  title: string;
  onPress: () => void;
  variant?: Variant;
  size?: Size;
  disabled?: boolean;
  loading?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
}

const AnimatedPressable = Animated.createAnimatedComponent(Pressable);

export function Button({
  title,
  onPress,
  variant = 'filled',
  size = 'md',
  disabled = false,
  loading = false,
  leftIcon,
  rightIcon,
}: ButtonProps) {
  const theme = useTheme();
  const scale = useSharedValue(1);

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
  }));

  const sizeStyles = {
    sm: { paddingVertical: 8, paddingHorizontal: 12, fontSize: 14 },
    md: { paddingVertical: 12, paddingHorizontal: 16, fontSize: 16 },
    lg: { paddingVertical: 16, paddingHorizontal: 24, fontSize: 18 },
  };

  const variantStyles = {
    filled: {
      backgroundColor: theme.colors.primary,
      textColor: '#ffffff',
    },
    outlined: {
      backgroundColor: 'transparent',
      borderWidth: 1,
      borderColor: theme.colors.primary,
      textColor: theme.colors.primary,
    },
    ghost: {
      backgroundColor: 'transparent',
      textColor: theme.colors.primary,
    },
  };

  const currentVariant = variantStyles[variant];
  const currentSize = sizeStyles[size];

  return (
    <AnimatedPressable
      style={[
        styles.base,
        {
          backgroundColor: currentVariant.backgroundColor,
          borderWidth: currentVariant.borderWidth,
          borderColor: currentVariant.borderColor,
          paddingVertical: currentSize.paddingVertical,
          paddingHorizontal: currentSize.paddingHorizontal,
          opacity: disabled ? 0.5 : 1,
        },
        animatedStyle,
      ]}
      onPress={onPress}
      onPressIn={() => { scale.value = withSpring(0.97); }}
      onPressOut={() => { scale.value = withSpring(1); }}
      disabled={disabled || loading}
    >
      {loading ? (
        <ActivityIndicator color={currentVariant.textColor} />
      ) : (
        <>
          {leftIcon}
          <Text
            style={{
              color: currentVariant.textColor,
              fontSize: currentSize.fontSize,
              fontWeight: '600',
              marginHorizontal: leftIcon || rightIcon ? 8 : 0,
            }}
          >
            {title}
          </Text>
          {rightIcon}
        </>
      )}
    </AnimatedPressable>
  );
}

const styles = StyleSheet.create({
  base: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    borderRadius: 8,
  },
});
```

## Form Styles

### Input Component

```typescript
import { useState } from 'react';
import {
  View,
  TextInput,
  StyleSheet,
  TextInputProps,
  Pressable,
} from 'react-native';
import { useTheme } from './theme';

interface InputProps extends TextInputProps {
  label?: string;
  error?: string;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
}

export function Input({
  label,
  error,
  leftIcon,
  rightIcon,
  style,
  ...props
}: InputProps) {
  const theme = useTheme();
  const [isFocused, setIsFocused] = useState(false);

  const borderColor = error
    ? theme.colors.error
    : isFocused
    ? theme.colors.primary
    : theme.colors.border;

  return (
    <View style={styles.container}>
      {label && (
        <Text style={[styles.label, { color: theme.colors.text }]}>
          {label}
        </Text>
      )}
      <View
        style={[
          styles.inputContainer,
          {
            borderColor,
            backgroundColor: theme.colors.surface,
          },
        ]}
      >
        {leftIcon && <View style={styles.icon}>{leftIcon}</View>}
        <TextInput
          style={[
            styles.input,
            { color: theme.colors.text },
            style,
          ]}
          placeholderTextColor={theme.colors.textSecondary}
          onFocus={() => setIsFocused(true)}
          onBlur={() => setIsFocused(false)}
          {...props}
        />
        {rightIcon && <View style={styles.icon}>{rightIcon}</View>}
      </View>
      {error && (
        <Text style={[styles.error, { color: theme.colors.error }]}>
          {error}
        </Text>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    marginBottom: 16,
  },
  label: {
    fontSize: 14,
    fontWeight: '500',
    marginBottom: 6,
  },
  inputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    borderWidth: 1,
    borderRadius: 8,
    paddingHorizontal: 12,
  },
  input: {
    flex: 1,
    paddingVertical: 12,
    fontSize: 16,
  },
  icon: {
    marginHorizontal: 4,
  },
  error: {
    fontSize: 12,
    marginTop: 4,
  },
});
```

## List Styles

### FlatList with Styling

```typescript
import { FlatList, View, StyleSheet } from 'react-native';

interface Item {
  id: string;
  title: string;
  subtitle: string;
}

function StyledList({ items }: { items: Item[] }) {
  return (
    <FlatList
      data={items}
      keyExtractor={(item) => item.id}
      renderItem={({ item, index }) => (
        <View
          style={[
            styles.item,
            index === 0 && styles.firstItem,
            index === items.length - 1 && styles.lastItem,
          ]}
        >
          <Text style={styles.itemTitle}>{item.title}</Text>
          <Text style={styles.itemSubtitle}>{item.subtitle}</Text>
        </View>
      )}
      ItemSeparatorComponent={() => <View style={styles.separator} />}
      ListHeaderComponent={() => (
        <Text style={styles.header}>List Header</Text>
      )}
      ListEmptyComponent={() => (
        <View style={styles.empty}>
          <Text>No items found</Text>
        </View>
      )}
      contentContainerStyle={styles.listContent}
    />
  );
}

const styles = StyleSheet.create({
  listContent: {
    padding: 16,
  },
  item: {
    backgroundColor: '#ffffff',
    padding: 16,
  },
  firstItem: {
    borderTopLeftRadius: 12,
    borderTopRightRadius: 12,
  },
  lastItem: {
    borderBottomLeftRadius: 12,
    borderBottomRightRadius: 12,
  },
  itemTitle: {
    fontSize: 16,
    fontWeight: '600',
    marginBottom: 4,
  },
  itemSubtitle: {
    fontSize: 14,
    color: '#6b7280',
  },
  separator: {
    height: 1,
    backgroundColor: '#e5e7eb',
  },
  header: {
    fontSize: 20,
    fontWeight: '700',
    marginBottom: 16,
  },
  empty: {
    alignItems: 'center',
    padding: 32,
  },
});
```
