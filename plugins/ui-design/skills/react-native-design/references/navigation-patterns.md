# React Navigation Patterns

## Setup and Configuration

### Installation

```bash
# Core packages
npm install @react-navigation/native
npm install @react-navigation/native-stack
npm install @react-navigation/bottom-tabs

# Required peer dependencies
npm install react-native-screens react-native-safe-area-context
```

### Type-Safe Navigation Setup

```typescript
// navigation/types.ts
import { NativeStackScreenProps } from "@react-navigation/native-stack";
import { BottomTabScreenProps } from "@react-navigation/bottom-tabs";
import {
  CompositeScreenProps,
  NavigatorScreenParams,
} from "@react-navigation/native";

// Define param lists for each navigator
export type RootStackParamList = {
  Main: NavigatorScreenParams<MainTabParamList>;
  Modal: { title: string };
  Auth: NavigatorScreenParams<AuthStackParamList>;
};

export type MainTabParamList = {
  Home: undefined;
  Search: { query?: string };
  Profile: { userId: string };
};

export type AuthStackParamList = {
  Login: undefined;
  Register: undefined;
  ForgotPassword: { email?: string };
};

// Screen props helpers
export type RootStackScreenProps<T extends keyof RootStackParamList> =
  NativeStackScreenProps<RootStackParamList, T>;

export type MainTabScreenProps<T extends keyof MainTabParamList> =
  CompositeScreenProps<
    BottomTabScreenProps<MainTabParamList, T>,
    RootStackScreenProps<keyof RootStackParamList>
  >;

// Global type declaration
declare global {
  namespace ReactNavigation {
    interface RootParamList extends RootStackParamList {}
  }
}
```

### Navigation Hooks

```typescript
// hooks/useAppNavigation.ts
import { useNavigation, useRoute, RouteProp } from "@react-navigation/native";
import { NativeStackNavigationProp } from "@react-navigation/native-stack";
import { RootStackParamList } from "./types";

export function useAppNavigation() {
  return useNavigation<NativeStackNavigationProp<RootStackParamList>>();
}

export function useTypedRoute<T extends keyof RootStackParamList>() {
  return useRoute<RouteProp<RootStackParamList, T>>();
}
```

## Stack Navigation

### Basic Stack Navigator

```typescript
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { RootStackParamList } from './types';

const Stack = createNativeStackNavigator<RootStackParamList>();

function RootNavigator() {
  return (
    <Stack.Navigator
      initialRouteName="Main"
      screenOptions={{
        headerStyle: { backgroundColor: '#6366f1' },
        headerTintColor: '#ffffff',
        headerTitleStyle: { fontWeight: '600' },
        headerBackTitleVisible: false,
        animation: 'slide_from_right',
      }}
    >
      <Stack.Screen
        name="Main"
        component={MainTabNavigator}
        options={{ headerShown: false }}
      />
      <Stack.Screen
        name="Modal"
        component={ModalScreen}
        options={{
          presentation: 'modal',
          animation: 'slide_from_bottom',
        }}
      />
      <Stack.Group screenOptions={{ presentation: 'fullScreenModal' }}>
        <Stack.Screen
          name="Auth"
          component={AuthNavigator}
          options={{ headerShown: false }}
        />
      </Stack.Group>
    </Stack.Navigator>
  );
}
```

### Screen with Dynamic Options

```typescript
function DetailScreen({ route, navigation }: DetailScreenProps) {
  const { itemId } = route.params;
  const [item, setItem] = useState<Item | null>(null);

  useEffect(() => {
    // Update header when data loads
    if (item) {
      navigation.setOptions({
        title: item.title,
        headerRight: () => (
          <TouchableOpacity onPress={() => shareItem(item)}>
            <Ionicons name="share-outline" size={24} color="#ffffff" />
          </TouchableOpacity>
        ),
      });
    }
  }, [item, navigation]);

  // Prevent going back with unsaved changes
  useEffect(() => {
    const unsubscribe = navigation.addListener('beforeRemove', (e) => {
      if (!hasUnsavedChanges) return;

      e.preventDefault();
      Alert.alert(
        'Discard changes?',
        'You have unsaved changes. Are you sure you want to leave?',
        [
          { text: "Don't leave", style: 'cancel' },
          {
            text: 'Discard',
            style: 'destructive',
            onPress: () => navigation.dispatch(e.data.action),
          },
        ]
      );
    });

    return unsubscribe;
  }, [navigation, hasUnsavedChanges]);

  return <View>{/* Content */}</View>;
}
```

## Tab Navigation

### Bottom Tab Navigator

```typescript
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { MainTabParamList } from './types';
import { Ionicons } from '@expo/vector-icons';

const Tab = createBottomTabNavigator<MainTabParamList>();

function MainTabNavigator() {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused, color, size }) => {
          const icons: Record<keyof MainTabParamList, string> = {
            Home: focused ? 'home' : 'home-outline',
            Search: focused ? 'search' : 'search-outline',
            Profile: focused ? 'person' : 'person-outline',
          };
          return (
            <Ionicons
              name={icons[route.name] as any}
              size={size}
              color={color}
            />
          );
        },
        tabBarActiveTintColor: '#6366f1',
        tabBarInactiveTintColor: '#9ca3af',
        tabBarStyle: {
          backgroundColor: '#ffffff',
          borderTopWidth: 1,
          borderTopColor: '#e5e7eb',
          paddingBottom: 8,
          paddingTop: 8,
          height: 60,
        },
        tabBarLabelStyle: {
          fontSize: 12,
          fontWeight: '500',
        },
        headerStyle: { backgroundColor: '#ffffff' },
        headerTitleStyle: { fontWeight: '600' },
      })}
    >
      <Tab.Screen
        name="Home"
        component={HomeScreen}
        options={{
          tabBarLabel: 'Home',
          tabBarBadge: 3,
        }}
      />
      <Tab.Screen
        name="Search"
        component={SearchScreen}
        options={{ tabBarLabel: 'Search' }}
      />
      <Tab.Screen
        name="Profile"
        component={ProfileScreen}
        options={{ tabBarLabel: 'Profile' }}
      />
    </Tab.Navigator>
  );
}
```

### Custom Tab Bar

```typescript
import { View, Pressable, StyleSheet } from 'react-native';
import { BottomTabBarProps } from '@react-navigation/bottom-tabs';
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withSpring,
} from 'react-native-reanimated';

function CustomTabBar({ state, descriptors, navigation }: BottomTabBarProps) {
  return (
    <View style={styles.tabBar}>
      {state.routes.map((route, index) => {
        const { options } = descriptors[route.key];
        const label = options.tabBarLabel ?? route.name;
        const isFocused = state.index === index;

        const onPress = () => {
          const event = navigation.emit({
            type: 'tabPress',
            target: route.key,
            canPreventDefault: true,
          });

          if (!isFocused && !event.defaultPrevented) {
            navigation.navigate(route.name);
          }
        };

        return (
          <TabBarButton
            key={route.key}
            label={label as string}
            isFocused={isFocused}
            onPress={onPress}
            icon={options.tabBarIcon}
          />
        );
      })}
    </View>
  );
}

function TabBarButton({ label, isFocused, onPress, icon }) {
  const scale = useSharedValue(1);

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
  }));

  return (
    <Pressable
      onPress={onPress}
      onPressIn={() => { scale.value = withSpring(0.9); }}
      onPressOut={() => { scale.value = withSpring(1); }}
      style={styles.tabButton}
    >
      <Animated.View style={animatedStyle}>
        {icon?.({
          focused: isFocused,
          color: isFocused ? '#6366f1' : '#9ca3af',
          size: 24,
        })}
        <Text
          style={[
            styles.tabLabel,
            { color: isFocused ? '#6366f1' : '#9ca3af' },
          ]}
        >
          {label}
        </Text>
      </Animated.View>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  tabBar: {
    flexDirection: 'row',
    backgroundColor: '#ffffff',
    paddingBottom: 20,
    paddingTop: 12,
    borderTopWidth: 1,
    borderTopColor: '#e5e7eb',
  },
  tabButton: {
    flex: 1,
    alignItems: 'center',
  },
  tabLabel: {
    fontSize: 12,
    marginTop: 4,
    fontWeight: '500',
  },
});

// Usage
<Tab.Navigator tabBar={(props) => <CustomTabBar {...props} />}>
  {/* screens */}
</Tab.Navigator>
```

## Drawer Navigation

```typescript
import {
  createDrawerNavigator,
  DrawerContentScrollView,
  DrawerItemList,
  DrawerContentComponentProps,
} from '@react-navigation/drawer';

const Drawer = createDrawerNavigator();

function CustomDrawerContent(props: DrawerContentComponentProps) {
  return (
    <DrawerContentScrollView {...props}>
      <View style={styles.drawerHeader}>
        <Image source={{ uri: user.avatar }} style={styles.avatar} />
        <Text style={styles.userName}>{user.name}</Text>
        <Text style={styles.userEmail}>{user.email}</Text>
      </View>
      <DrawerItemList {...props} />
      <View style={styles.drawerFooter}>
        <TouchableOpacity
          onPress={handleLogout}
          style={styles.logoutButton}
        >
          <Ionicons name="log-out-outline" size={24} color="#ef4444" />
          <Text style={styles.logoutText}>Log Out</Text>
        </TouchableOpacity>
      </View>
    </DrawerContentScrollView>
  );
}

function DrawerNavigator() {
  return (
    <Drawer.Navigator
      drawerContent={(props) => <CustomDrawerContent {...props} />}
      screenOptions={{
        drawerActiveBackgroundColor: '#ede9fe',
        drawerActiveTintColor: '#6366f1',
        drawerInactiveTintColor: '#4b5563',
        drawerLabelStyle: { marginLeft: -20, fontSize: 15, fontWeight: '500' },
        drawerStyle: { width: 280 },
      }}
    >
      <Drawer.Screen
        name="Home"
        component={HomeScreen}
        options={{
          drawerIcon: ({ color }) => (
            <Ionicons name="home-outline" size={22} color={color} />
          ),
        }}
      />
      <Drawer.Screen
        name="Settings"
        component={SettingsScreen}
        options={{
          drawerIcon: ({ color }) => (
            <Ionicons name="settings-outline" size={22} color={color} />
          ),
        }}
      />
    </Drawer.Navigator>
  );
}
```

## Deep Linking

### Configuration

```typescript
// navigation/linking.ts
import { LinkingOptions } from '@react-navigation/native';
import { RootStackParamList } from './types';

export const linking: LinkingOptions<RootStackParamList> = {
  prefixes: ['myapp://', 'https://myapp.com'],
  config: {
    screens: {
      Main: {
        screens: {
          Home: 'home',
          Search: 'search',
          Profile: 'profile/:userId',
        },
      },
      Modal: 'modal/:title',
      Auth: {
        screens: {
          Login: 'login',
          Register: 'register',
          ForgotPassword: 'forgot-password',
        },
      },
    },
  },
  // Custom URL parsing
  getStateFromPath: (path, config) => {
    // Handle custom URL patterns
    return getStateFromPath(path, config);
  },
};

// App.tsx
function App() {
  return (
    <NavigationContainer linking={linking} fallback={<LoadingScreen />}>
      <RootNavigator />
    </NavigationContainer>
  );
}
```

### Handling Deep Links

```typescript
import { useEffect } from "react";
import { Linking } from "react-native";
import { useNavigation } from "@react-navigation/native";

function useDeepLinkHandler() {
  const navigation = useNavigation();

  useEffect(() => {
    // Handle initial URL
    const handleInitialUrl = async () => {
      const url = await Linking.getInitialURL();
      if (url) {
        handleDeepLink(url);
      }
    };

    // Handle URL changes
    const subscription = Linking.addEventListener("url", ({ url }) => {
      handleDeepLink(url);
    });

    handleInitialUrl();

    return () => subscription.remove();
  }, []);

  const handleDeepLink = (url: string) => {
    // Parse URL and navigate
    const route = parseUrl(url);
    if (route) {
      navigation.navigate(route.name, route.params);
    }
  };
}
```

## Navigation State Management

### Auth Flow

```typescript
import { createContext, useContext, useState, useEffect } from 'react';

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  signIn: (email: string, password: string) => Promise<void>;
  signOut: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType>(null!);

function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check for existing session
    checkAuthState();
  }, []);

  const checkAuthState = async () => {
    try {
      const token = await AsyncStorage.getItem('token');
      if (token) {
        const user = await fetchUser(token);
        setUser(user);
      }
    } catch (error) {
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  const signIn = async (email: string, password: string) => {
    const { user, token } = await loginApi(email, password);
    await AsyncStorage.setItem('token', token);
    setUser(user);
  };

  const signOut = async () => {
    await AsyncStorage.removeItem('token');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, isLoading, signIn, signOut }}>
      {children}
    </AuthContext.Provider>
  );
}

function RootNavigator() {
  const { user, isLoading } = useAuth();

  if (isLoading) {
    return <SplashScreen />;
  }

  return (
    <Stack.Navigator screenOptions={{ headerShown: false }}>
      {user ? (
        <Stack.Screen name="Main" component={MainNavigator} />
      ) : (
        <Stack.Screen name="Auth" component={AuthNavigator} />
      )}
    </Stack.Navigator>
  );
}
```

### Navigation State Persistence

```typescript
import AsyncStorage from '@react-native-async-storage/async-storage';
import { NavigationContainer, NavigationState } from '@react-navigation/native';

const PERSISTENCE_KEY = 'NAVIGATION_STATE';

function App() {
  const [isReady, setIsReady] = useState(false);
  const [initialState, setInitialState] = useState<NavigationState | undefined>();

  useEffect(() => {
    const restoreState = async () => {
      try {
        const savedState = await AsyncStorage.getItem(PERSISTENCE_KEY);
        if (savedState) {
          setInitialState(JSON.parse(savedState));
        }
      } catch (e) {
        console.error('Failed to restore navigation state:', e);
      } finally {
        setIsReady(true);
      }
    };

    if (!isReady) {
      restoreState();
    }
  }, [isReady]);

  if (!isReady) {
    return <SplashScreen />;
  }

  return (
    <NavigationContainer
      initialState={initialState}
      onStateChange={(state) => {
        AsyncStorage.setItem(PERSISTENCE_KEY, JSON.stringify(state));
      }}
    >
      <RootNavigator />
    </NavigationContainer>
  );
}
```

## Screen Transitions

### Custom Animations

```typescript
import { TransitionPresets } from '@react-navigation/native-stack';

<Stack.Navigator
  screenOptions={{
    ...TransitionPresets.SlideFromRightIOS,
    gestureEnabled: true,
    gestureDirection: 'horizontal',
  }}
>
  {/* Standard slide transition */}
  <Stack.Screen name="List" component={ListScreen} />

  {/* Modal with custom animation */}
  <Stack.Screen
    name="Modal"
    component={ModalScreen}
    options={{
      presentation: 'transparentModal',
      animation: 'fade',
      cardOverlayEnabled: true,
    }}
  />

  {/* Full screen modal */}
  <Stack.Screen
    name="FullScreenModal"
    component={FullScreenModalScreen}
    options={{
      presentation: 'fullScreenModal',
      animation: 'slide_from_bottom',
    }}
  />
</Stack.Navigator>
```

### Shared Element Transitions

```typescript
import { SharedElement } from 'react-navigation-shared-element';
import { createSharedElementStackNavigator } from 'react-navigation-shared-element';

const Stack = createSharedElementStackNavigator();

function ListScreen({ navigation }) {
  return (
    <FlatList
      data={items}
      renderItem={({ item }) => (
        <Pressable onPress={() => navigation.navigate('Detail', { item })}>
          <SharedElement id={`item.${item.id}.photo`}>
            <Image source={{ uri: item.imageUrl }} style={styles.image} />
          </SharedElement>
          <SharedElement id={`item.${item.id}.title`}>
            <Text style={styles.title}>{item.title}</Text>
          </SharedElement>
        </Pressable>
      )}
    />
  );
}

function DetailScreen({ route }) {
  const { item } = route.params;

  return (
    <View>
      <SharedElement id={`item.${item.id}.photo`}>
        <Image source={{ uri: item.imageUrl }} style={styles.heroImage} />
      </SharedElement>
      <SharedElement id={`item.${item.id}.title`}>
        <Text style={styles.title}>{item.title}</Text>
      </SharedElement>
    </View>
  );
}

// Navigator configuration
<Stack.Navigator>
  <Stack.Screen name="List" component={ListScreen} />
  <Stack.Screen
    name="Detail"
    component={DetailScreen}
    sharedElements={(route) => {
      const { item } = route.params;
      return [
        { id: `item.${item.id}.photo`, animation: 'move' },
        { id: `item.${item.id}.title`, animation: 'fade' },
      ];
    }}
  />
</Stack.Navigator>
```

## Header Customization

### Custom Header Component

```typescript
import { getHeaderTitle } from '@react-navigation/elements';
import { NativeStackHeaderProps } from '@react-navigation/native-stack';

function CustomHeader({ navigation, route, options, back }: NativeStackHeaderProps) {
  const title = getHeaderTitle(options, route.name);

  return (
    <View style={styles.header}>
      {back && (
        <TouchableOpacity
          onPress={navigation.goBack}
          style={styles.backButton}
        >
          <Ionicons name="arrow-back" size={24} color="#1f2937" />
        </TouchableOpacity>
      )}
      <Text style={styles.title}>{title}</Text>
      {options.headerRight && (
        <View style={styles.rightActions}>
          {options.headerRight({ canGoBack: !!back })}
        </View>
      )}
    </View>
  );
}

// Usage
<Stack.Navigator
  screenOptions={{
    header: (props) => <CustomHeader {...props} />,
  }}
>
  {/* screens */}
</Stack.Navigator>
```

### Collapsible Header

```typescript
import Animated, {
  useSharedValue,
  useAnimatedScrollHandler,
  useAnimatedStyle,
  interpolate,
  Extrapolation,
} from 'react-native-reanimated';

const HEADER_HEIGHT = 200;
const COLLAPSED_HEIGHT = 60;

function CollapsibleHeaderScreen() {
  const scrollY = useSharedValue(0);

  const scrollHandler = useAnimatedScrollHandler({
    onScroll: (event) => {
      scrollY.value = event.contentOffset.y;
    },
  });

  const headerStyle = useAnimatedStyle(() => {
    const height = interpolate(
      scrollY.value,
      [0, HEADER_HEIGHT - COLLAPSED_HEIGHT],
      [HEADER_HEIGHT, COLLAPSED_HEIGHT],
      Extrapolation.CLAMP
    );

    return { height };
  });

  const titleStyle = useAnimatedStyle(() => {
    const fontSize = interpolate(
      scrollY.value,
      [0, HEADER_HEIGHT - COLLAPSED_HEIGHT],
      [32, 18],
      Extrapolation.CLAMP
    );

    return { fontSize };
  });

  return (
    <View style={styles.container}>
      <Animated.View style={[styles.header, headerStyle]}>
        <Animated.Text style={[styles.title, titleStyle]}>
          Title
        </Animated.Text>
      </Animated.View>

      <Animated.ScrollView
        onScroll={scrollHandler}
        scrollEventThrottle={16}
        contentContainerStyle={{ paddingTop: HEADER_HEIGHT }}
      >
        {/* Content */}
      </Animated.ScrollView>
    </View>
  );
}
```
