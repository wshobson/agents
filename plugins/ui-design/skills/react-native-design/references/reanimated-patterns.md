# React Native Reanimated 3 Patterns

## Core Concepts

### Shared Values and Animated Styles

```typescript
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withSpring,
  withTiming,
  withDelay,
  withSequence,
  withRepeat,
  Easing,
} from 'react-native-reanimated';

function BasicAnimations() {
  // Shared value - can be modified from JS or UI thread
  const opacity = useSharedValue(0);
  const scale = useSharedValue(1);
  const rotation = useSharedValue(0);

  // Animated style - runs on UI thread
  const animatedStyle = useAnimatedStyle(() => ({
    opacity: opacity.value,
    transform: [
      { scale: scale.value },
      { rotate: `${rotation.value}deg` },
    ],
  }));

  const animate = () => {
    // Spring animation
    scale.value = withSpring(1.2, {
      damping: 10,
      stiffness: 100,
    });

    // Timing animation with easing
    opacity.value = withTiming(1, {
      duration: 500,
      easing: Easing.bezier(0.25, 0.1, 0.25, 1),
    });

    // Sequence of animations
    rotation.value = withSequence(
      withTiming(15, { duration: 100 }),
      withTiming(-15, { duration: 100 }),
      withTiming(0, { duration: 100 })
    );
  };

  return (
    <Animated.View style={[styles.box, animatedStyle]} />
  );
}
```

### Animation Callbacks

```typescript
import { runOnJS, runOnUI } from 'react-native-reanimated';

function AnimationWithCallbacks() {
  const translateX = useSharedValue(0);
  const [status, setStatus] = useState('idle');

  const updateStatus = (newStatus: string) => {
    setStatus(newStatus);
  };

  const animate = () => {
    translateX.value = withTiming(
      200,
      { duration: 1000 },
      (finished) => {
        'worklet';
        if (finished) {
          // Call JS function from worklet
          runOnJS(updateStatus)('completed');
        }
      }
    );
  };

  return (
    <Animated.View
      style={[
        styles.box,
        useAnimatedStyle(() => ({
          transform: [{ translateX: translateX.value }],
        })),
      ]}
    />
  );
}
```

## Gesture Handler Integration

### Pan Gesture

```typescript
import { Gesture, GestureDetector } from 'react-native-gesture-handler';
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withSpring,
  clamp,
} from 'react-native-reanimated';

function DraggableBox() {
  const translateX = useSharedValue(0);
  const translateY = useSharedValue(0);
  const context = useSharedValue({ x: 0, y: 0 });

  const panGesture = Gesture.Pan()
    .onStart(() => {
      context.value = { x: translateX.value, y: translateY.value };
    })
    .onUpdate((event) => {
      translateX.value = event.translationX + context.value.x;
      translateY.value = event.translationY + context.value.y;
    })
    .onEnd((event) => {
      // Apply velocity decay
      translateX.value = withSpring(
        clamp(translateX.value + event.velocityX / 10, -100, 100)
      );
      translateY.value = withSpring(
        clamp(translateY.value + event.velocityY / 10, -100, 100)
      );
    });

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [
      { translateX: translateX.value },
      { translateY: translateY.value },
    ],
  }));

  return (
    <GestureDetector gesture={panGesture}>
      <Animated.View style={[styles.box, animatedStyle]} />
    </GestureDetector>
  );
}
```

### Pinch and Rotate Gestures

```typescript
function ZoomableImage() {
  const scale = useSharedValue(1);
  const rotation = useSharedValue(0);
  const savedScale = useSharedValue(1);
  const savedRotation = useSharedValue(0);

  const pinchGesture = Gesture.Pinch()
    .onUpdate((event) => {
      scale.value = savedScale.value * event.scale;
    })
    .onEnd(() => {
      savedScale.value = scale.value;
      // Snap back if too small
      if (scale.value < 1) {
        scale.value = withSpring(1);
        savedScale.value = 1;
      }
    });

  const rotateGesture = Gesture.Rotation()
    .onUpdate((event) => {
      rotation.value = savedRotation.value + event.rotation;
    })
    .onEnd(() => {
      savedRotation.value = rotation.value;
    });

  const composed = Gesture.Simultaneous(pinchGesture, rotateGesture);

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [
      { scale: scale.value },
      { rotate: `${rotation.value}rad` },
    ],
  }));

  return (
    <GestureDetector gesture={composed}>
      <Animated.Image
        source={{ uri: imageUrl }}
        style={[styles.image, animatedStyle]}
      />
    </GestureDetector>
  );
}
```

### Tap Gesture with Feedback

```typescript
function TappableCard({ onPress, children }: TappableCardProps) {
  const scale = useSharedValue(1);
  const opacity = useSharedValue(1);

  const tapGesture = Gesture.Tap()
    .onBegin(() => {
      scale.value = withSpring(0.97);
      opacity.value = withTiming(0.8, { duration: 100 });
    })
    .onFinalize(() => {
      scale.value = withSpring(1);
      opacity.value = withTiming(1, { duration: 100 });
    })
    .onEnd(() => {
      runOnJS(onPress)();
    });

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
    opacity: opacity.value,
  }));

  return (
    <GestureDetector gesture={tapGesture}>
      <Animated.View style={[styles.card, animatedStyle]}>
        {children}
      </Animated.View>
    </GestureDetector>
  );
}
```

## Common Animation Patterns

### Fade In/Out

```typescript
function FadeInView({ visible, children }: FadeInViewProps) {
  const opacity = useSharedValue(0);

  useEffect(() => {
    opacity.value = withTiming(visible ? 1 : 0, { duration: 300 });
  }, [visible]);

  const animatedStyle = useAnimatedStyle(() => ({
    opacity: opacity.value,
    display: opacity.value === 0 ? 'none' : 'flex',
  }));

  return (
    <Animated.View style={animatedStyle}>
      {children}
    </Animated.View>
  );
}
```

### Slide In/Out

```typescript
function SlideInView({ visible, direction = 'right', children }) {
  const translateX = useSharedValue(direction === 'right' ? 100 : -100);
  const opacity = useSharedValue(0);

  useEffect(() => {
    if (visible) {
      translateX.value = withSpring(0);
      opacity.value = withTiming(1);
    } else {
      translateX.value = withSpring(direction === 'right' ? 100 : -100);
      opacity.value = withTiming(0);
    }
  }, [visible, direction]);

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ translateX: translateX.value }],
    opacity: opacity.value,
  }));

  return (
    <Animated.View style={animatedStyle}>
      {children}
    </Animated.View>
  );
}
```

### Staggered List Animation

```typescript
function StaggeredList({ items }: { items: Item[] }) {
  return (
    <FlatList
      data={items}
      keyExtractor={(item) => item.id}
      renderItem={({ item, index }) => (
        <StaggeredItem item={item} index={index} />
      )}
    />
  );
}

function StaggeredItem({ item, index }: { item: Item; index: number }) {
  const translateY = useSharedValue(50);
  const opacity = useSharedValue(0);

  useEffect(() => {
    translateY.value = withDelay(
      index * 100,
      withSpring(0, { damping: 15 })
    );
    opacity.value = withDelay(
      index * 100,
      withTiming(1, { duration: 300 })
    );
  }, [index]);

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ translateY: translateY.value }],
    opacity: opacity.value,
  }));

  return (
    <Animated.View style={[styles.listItem, animatedStyle]}>
      <Text>{item.title}</Text>
    </Animated.View>
  );
}
```

### Pulse Animation

```typescript
function PulseView({ children }: { children: React.ReactNode }) {
  const scale = useSharedValue(1);

  useEffect(() => {
    scale.value = withRepeat(
      withSequence(
        withTiming(1.05, { duration: 500 }),
        withTiming(1, { duration: 500 })
      ),
      -1, // infinite
      false // no reverse
    );

    return () => {
      cancelAnimation(scale);
    };
  }, []);

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
  }));

  return (
    <Animated.View style={animatedStyle}>
      {children}
    </Animated.View>
  );
}
```

### Shake Animation

```typescript
function ShakeView({ trigger, children }) {
  const translateX = useSharedValue(0);

  useEffect(() => {
    if (trigger) {
      translateX.value = withSequence(
        withTiming(-10, { duration: 50 }),
        withTiming(10, { duration: 50 }),
        withTiming(-10, { duration: 50 }),
        withTiming(10, { duration: 50 }),
        withTiming(0, { duration: 50 })
      );
    }
  }, [trigger]);

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ translateX: translateX.value }],
  }));

  return (
    <Animated.View style={animatedStyle}>
      {children}
    </Animated.View>
  );
}
```

## Advanced Patterns

### Interpolation

```typescript
import { interpolate, Extrapolation } from 'react-native-reanimated';

function ParallaxHeader() {
  const scrollY = useSharedValue(0);

  const headerStyle = useAnimatedStyle(() => {
    const height = interpolate(
      scrollY.value,
      [0, 200],
      [300, 100],
      Extrapolation.CLAMP
    );

    const opacity = interpolate(
      scrollY.value,
      [0, 150, 200],
      [1, 0.5, 0],
      Extrapolation.CLAMP
    );

    const translateY = interpolate(
      scrollY.value,
      [0, 200],
      [0, -50],
      Extrapolation.CLAMP
    );

    return {
      height,
      opacity,
      transform: [{ translateY }],
    };
  });

  return (
    <View style={styles.container}>
      <Animated.View style={[styles.header, headerStyle]}>
        <Text style={styles.headerTitle}>Header</Text>
      </Animated.View>
      <Animated.ScrollView
        onScroll={useAnimatedScrollHandler({
          onScroll: (event) => {
            scrollY.value = event.contentOffset.y;
          },
        })}
        scrollEventThrottle={16}
      >
        {/* Content */}
      </Animated.ScrollView>
    </View>
  );
}
```

### Color Interpolation

```typescript
import { interpolateColor } from 'react-native-reanimated';

function ColorTransition() {
  const progress = useSharedValue(0);

  const animatedStyle = useAnimatedStyle(() => {
    const backgroundColor = interpolateColor(
      progress.value,
      [0, 0.5, 1],
      ['#6366f1', '#8b5cf6', '#ec4899']
    );

    return { backgroundColor };
  });

  const toggleColor = () => {
    progress.value = withTiming(progress.value === 0 ? 1 : 0, {
      duration: 1000,
    });
  };

  return (
    <Pressable onPress={toggleColor}>
      <Animated.View style={[styles.box, animatedStyle]} />
    </Pressable>
  );
}
```

### Derived Values

```typescript
import { useDerivedValue } from 'react-native-reanimated';

function DerivedValueExample() {
  const x = useSharedValue(0);
  const y = useSharedValue(0);

  // Derived value computed from other shared values
  const distance = useDerivedValue(() => {
    return Math.sqrt(x.value ** 2 + y.value ** 2);
  });

  const angle = useDerivedValue(() => {
    return Math.atan2(y.value, x.value) * (180 / Math.PI);
  });

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [
      { translateX: x.value },
      { translateY: y.value },
      { rotate: `${angle.value}deg` },
    ],
    opacity: interpolate(distance.value, [0, 200], [1, 0.5]),
  }));

  return (
    <Animated.View style={[styles.box, animatedStyle]} />
  );
}
```

### Layout Animations

```typescript
import Animated, {
  Layout,
  FadeIn,
  FadeOut,
  SlideInLeft,
  SlideOutRight,
  ZoomIn,
  ZoomOut,
} from 'react-native-reanimated';

function AnimatedList() {
  const [items, setItems] = useState([1, 2, 3, 4, 5]);

  const addItem = () => {
    setItems([...items, items.length + 1]);
  };

  const removeItem = (id: number) => {
    setItems(items.filter((item) => item !== id));
  };

  return (
    <View style={styles.container}>
      <Button title="Add Item" onPress={addItem} />
      {items.map((item) => (
        <Animated.View
          key={item}
          style={styles.item}
          entering={FadeIn.duration(300).springify()}
          exiting={SlideOutRight.duration(300)}
          layout={Layout.springify()}
        >
          <Text>Item {item}</Text>
          <Pressable onPress={() => removeItem(item)}>
            <Text>Remove</Text>
          </Pressable>
        </Animated.View>
      ))}
    </View>
  );
}
```

### Swipeable Card

```typescript
function SwipeableCard({ onSwipeLeft, onSwipeRight }) {
  const translateX = useSharedValue(0);
  const rotateZ = useSharedValue(0);
  const context = useSharedValue({ x: 0 });

  const SWIPE_THRESHOLD = 120;

  const panGesture = Gesture.Pan()
    .onStart(() => {
      context.value = { x: translateX.value };
    })
    .onUpdate((event) => {
      translateX.value = event.translationX + context.value.x;
      rotateZ.value = interpolate(
        translateX.value,
        [-200, 0, 200],
        [-15, 0, 15]
      );
    })
    .onEnd((event) => {
      if (translateX.value > SWIPE_THRESHOLD) {
        translateX.value = withTiming(500, { duration: 200 }, () => {
          runOnJS(onSwipeRight)();
        });
      } else if (translateX.value < -SWIPE_THRESHOLD) {
        translateX.value = withTiming(-500, { duration: 200 }, () => {
          runOnJS(onSwipeLeft)();
        });
      } else {
        translateX.value = withSpring(0);
        rotateZ.value = withSpring(0);
      }
    });

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [
      { translateX: translateX.value },
      { rotate: `${rotateZ.value}deg` },
    ],
  }));

  const leftIndicatorStyle = useAnimatedStyle(() => ({
    opacity: interpolate(
      translateX.value,
      [0, SWIPE_THRESHOLD],
      [0, 1],
      Extrapolation.CLAMP
    ),
  }));

  const rightIndicatorStyle = useAnimatedStyle(() => ({
    opacity: interpolate(
      translateX.value,
      [-SWIPE_THRESHOLD, 0],
      [1, 0],
      Extrapolation.CLAMP
    ),
  }));

  return (
    <GestureDetector gesture={panGesture}>
      <Animated.View style={[styles.card, animatedStyle]}>
        <Animated.View style={[styles.likeIndicator, leftIndicatorStyle]}>
          <Text>LIKE</Text>
        </Animated.View>
        <Animated.View style={[styles.nopeIndicator, rightIndicatorStyle]}>
          <Text>NOPE</Text>
        </Animated.View>
        {/* Card content */}
      </Animated.View>
    </GestureDetector>
  );
}
```

### Bottom Sheet

```typescript
const MAX_TRANSLATE_Y = -SCREEN_HEIGHT + 50;
const MIN_TRANSLATE_Y = 0;
const SNAP_POINTS = [-SCREEN_HEIGHT * 0.5, -SCREEN_HEIGHT * 0.25, 0];

function BottomSheet({ children }) {
  const translateY = useSharedValue(0);
  const context = useSharedValue({ y: 0 });

  const panGesture = Gesture.Pan()
    .onStart(() => {
      context.value = { y: translateY.value };
    })
    .onUpdate((event) => {
      translateY.value = clamp(
        context.value.y + event.translationY,
        MAX_TRANSLATE_Y,
        MIN_TRANSLATE_Y
      );
    })
    .onEnd((event) => {
      // Find closest snap point
      const destination = SNAP_POINTS.reduce((prev, curr) =>
        Math.abs(curr - translateY.value) < Math.abs(prev - translateY.value)
          ? curr
          : prev
      );

      translateY.value = withSpring(destination, {
        damping: 50,
        stiffness: 300,
      });
    });

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ translateY: translateY.value }],
  }));

  const backdropStyle = useAnimatedStyle(() => ({
    opacity: interpolate(
      translateY.value,
      [MIN_TRANSLATE_Y, MAX_TRANSLATE_Y],
      [0, 0.5]
    ),
    pointerEvents: translateY.value < -50 ? 'auto' : 'none',
  }));

  return (
    <>
      <Animated.View style={[styles.backdrop, backdropStyle]} />
      <GestureDetector gesture={panGesture}>
        <Animated.View style={[styles.bottomSheet, animatedStyle]}>
          <View style={styles.handle} />
          {children}
        </Animated.View>
      </GestureDetector>
    </>
  );
}
```

## Performance Tips

### Memoization

```typescript
// Memoize animated style when dependencies don't change
const animatedStyle = useAnimatedStyle(
  () => ({
    transform: [{ translateX: translateX.value }],
  }),
  [],
); // Empty deps if no external dependencies

// Use useMemo for complex calculations outside worklets
const threshold = useMemo(() => calculateThreshold(screenWidth), [screenWidth]);
```

### Worklet Best Practices

```typescript
// Do: Keep worklets simple
const simpleWorklet = () => {
  "worklet";
  return scale.value * 2;
};

// Don't: Complex logic in worklets
// Move complex logic to JS with runOnJS

// Do: Use runOnJS for callbacks
const onComplete = () => {
  setIsAnimating(false);
};

opacity.value = withTiming(1, {}, (finished) => {
  "worklet";
  if (finished) {
    runOnJS(onComplete)();
  }
});
```

### Cancel Animations

```typescript
import { cancelAnimation } from 'react-native-reanimated';

function AnimatedComponent() {
  const translateX = useSharedValue(0);

  useEffect(() => {
    // Start animation
    translateX.value = withRepeat(
      withTiming(100, { duration: 1000 }),
      -1,
      true
    );

    // Cleanup: cancel animation on unmount
    return () => {
      cancelAnimation(translateX);
    };
  }, []);

  return <Animated.View style={animatedStyle} />;
}
```
