# Dart/Flutter Style Guide

Dart language conventions and Flutter-specific patterns.

## Null Safety

### Enable Sound Null Safety

```dart
// pubspec.yaml
environment:
  sdk: '>=3.0.0 <4.0.0'

// All types are non-nullable by default
String name = 'John';      // Cannot be null
String? nickname;          // Can be null

// Late initialization
late final Database database;
```

### Null-Aware Operators

```dart
// Null-aware access
final length = user?.name?.length;

// Null-aware assignment
nickname ??= 'Anonymous';

// Null assertion (use sparingly)
final definitelyNotNull = maybeNull!;

// Null-aware cascade
user
  ?..name = 'John'
  ..email = 'john@example.com';

// Null coalescing
final displayName = user.nickname ?? user.name ?? 'Unknown';
```

### Null Handling Patterns

```dart
// Guard clause with null check
void processUser(User? user) {
  if (user == null) {
    throw ArgumentError('User cannot be null');
  }
  // user is promoted to non-nullable here
  print(user.name);
}

// Pattern matching (Dart 3)
void handleResult(Result? result) {
  switch (result) {
    case Success(data: final data):
      handleSuccess(data);
    case Error(message: final message):
      handleError(message);
    case null:
      handleNull();
  }
}
```

## Async/Await

### Future Basics

```dart
// Async function
Future<User> fetchUser(int id) async {
  final response = await http.get(Uri.parse('/users/$id'));
  if (response.statusCode != 200) {
    throw HttpException('Failed to fetch user');
  }
  return User.fromJson(jsonDecode(response.body));
}

// Error handling
Future<User?> safeFetchUser(int id) async {
  try {
    return await fetchUser(id);
  } on HttpException catch (e) {
    logger.error('HTTP error: ${e.message}');
    return null;
  } catch (e) {
    logger.error('Unexpected error: $e');
    return null;
  }
}
```

### Parallel Execution

```dart
// Wait for all futures
Future<Dashboard> loadDashboard() async {
  final results = await Future.wait([
    fetchUsers(),
    fetchOrders(),
    fetchStats(),
  ]);

  return Dashboard(
    users: results[0] as List<User>,
    orders: results[1] as List<Order>,
    stats: results[2] as Stats,
  );
}

// With typed results
Future<(List<User>, List<Order>)> loadData() async {
  final (users, orders) = await (
    fetchUsers(),
    fetchOrders(),
  ).wait;
  return (users, orders);
}
```

### Streams

```dart
// Stream creation
Stream<int> countStream(int max) async* {
  for (var i = 0; i < max; i++) {
    await Future.delayed(const Duration(seconds: 1));
    yield i;
  }
}

// Stream transformation
Stream<String> userNames(Stream<User> users) {
  return users.map((user) => user.name);
}

// Stream consumption
void listenToUsers() {
  userStream.listen(
    (user) => print('New user: ${user.name}'),
    onError: (error) => print('Error: $error'),
    onDone: () => print('Stream closed'),
  );
}
```

## Widgets

### Stateless Widgets

```dart
class UserCard extends StatelessWidget {
  const UserCard({
    super.key,
    required this.user,
    this.onTap,
  });

  final User user;
  final VoidCallback? onTap;

  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        leading: CircleAvatar(
          backgroundImage: NetworkImage(user.avatarUrl),
        ),
        title: Text(user.name),
        subtitle: Text(user.email),
        onTap: onTap,
      ),
    );
  }
}
```

### Stateful Widgets

```dart
class Counter extends StatefulWidget {
  const Counter({super.key, this.initialValue = 0});

  final int initialValue;

  @override
  State<Counter> createState() => _CounterState();
}

class _CounterState extends State<Counter> {
  late int _count;

  @override
  void initState() {
    super.initState();
    _count = widget.initialValue;
  }

  void _increment() {
    setState(() {
      _count++;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text('Count: $_count'),
        ElevatedButton(
          onPressed: _increment,
          child: const Text('Increment'),
        ),
      ],
    );
  }
}
```

### Widget Best Practices

```dart
// Use const constructors
class MyWidget extends StatelessWidget {
  const MyWidget({super.key}); // const constructor

  @override
  Widget build(BuildContext context) {
    return const Column(
      children: [
        Text('Hello'),        // const widget
        SizedBox(height: 8),  // const widget
      ],
    );
  }
}

// Extract widgets for reusability
class PrimaryButton extends StatelessWidget {
  const PrimaryButton({
    super.key,
    required this.label,
    required this.onPressed,
    this.isLoading = false,
  });

  final String label;
  final VoidCallback? onPressed;
  final bool isLoading;

  @override
  Widget build(BuildContext context) {
    return ElevatedButton(
      onPressed: isLoading ? null : onPressed,
      child: isLoading
          ? const SizedBox(
              width: 20,
              height: 20,
              child: CircularProgressIndicator(strokeWidth: 2),
            )
          : Text(label),
    );
  }
}
```

## State Management

### Provider Pattern

```dart
// Model with ChangeNotifier
class CartModel extends ChangeNotifier {
  final List<Item> _items = [];

  List<Item> get items => List.unmodifiable(_items);

  double get totalPrice => _items.fold(0, (sum, item) => sum + item.price);

  void addItem(Item item) {
    _items.add(item);
    notifyListeners();
  }

  void removeItem(Item item) {
    _items.remove(item);
    notifyListeners();
  }
}

// Provider setup
void main() {
  runApp(
    ChangeNotifierProvider(
      create: (_) => CartModel(),
      child: const MyApp(),
    ),
  );
}

// Consuming provider
class CartPage extends StatelessWidget {
  const CartPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Consumer<CartModel>(
      builder: (context, cart, child) {
        return ListView.builder(
          itemCount: cart.items.length,
          itemBuilder: (context, index) {
            return ListTile(
              title: Text(cart.items[index].name),
            );
          },
        );
      },
    );
  }
}
```

### Riverpod Pattern

```dart
// Provider definition
final userProvider = FutureProvider<User>((ref) async {
  final repository = ref.read(userRepositoryProvider);
  return repository.fetchCurrentUser();
});

final counterProvider = StateNotifierProvider<CounterNotifier, int>((ref) {
  return CounterNotifier();
});

class CounterNotifier extends StateNotifier<int> {
  CounterNotifier() : super(0);

  void increment() => state++;
  void decrement() => state--;
}

// Consumer widget
class UserProfile extends ConsumerWidget {
  const UserProfile({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final userAsync = ref.watch(userProvider);

    return userAsync.when(
      data: (user) => Text('Hello, ${user.name}'),
      loading: () => const CircularProgressIndicator(),
      error: (error, stack) => Text('Error: $error'),
    );
  }
}
```

### BLoC Pattern

```dart
// Events
abstract class CounterEvent {}
class IncrementEvent extends CounterEvent {}
class DecrementEvent extends CounterEvent {}

// State
class CounterState {
  final int count;
  const CounterState(this.count);
}

// BLoC
class CounterBloc extends Bloc<CounterEvent, CounterState> {
  CounterBloc() : super(const CounterState(0)) {
    on<IncrementEvent>((event, emit) {
      emit(CounterState(state.count + 1));
    });

    on<DecrementEvent>((event, emit) {
      emit(CounterState(state.count - 1));
    });
  }
}

// Usage
class CounterPage extends StatelessWidget {
  const CounterPage({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocBuilder<CounterBloc, CounterState>(
      builder: (context, state) {
        return Text('Count: ${state.count}');
      },
    );
  }
}
```

## Testing

### Unit Tests

```dart
import 'package:test/test.dart';

void main() {
  group('Calculator', () {
    late Calculator calculator;

    setUp(() {
      calculator = Calculator();
    });

    test('adds two positive numbers', () {
      expect(calculator.add(2, 3), equals(5));
    });

    test('handles negative numbers', () {
      expect(calculator.add(-1, 1), equals(0));
    });
  });
}
```

### Widget Tests

```dart
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('Counter increments', (WidgetTester tester) async {
    // Build widget
    await tester.pumpWidget(const MaterialApp(home: Counter()));

    // Verify initial state
    expect(find.text('Count: 0'), findsOneWidget);

    // Tap increment button
    await tester.tap(find.byIcon(Icons.add));
    await tester.pump();

    // Verify incremented state
    expect(find.text('Count: 1'), findsOneWidget);
  });

  testWidgets('shows loading indicator', (WidgetTester tester) async {
    await tester.pumpWidget(
      const MaterialApp(
        home: UserProfile(isLoading: true),
      ),
    );

    expect(find.byType(CircularProgressIndicator), findsOneWidget);
  });
}
```

### Mocking

```dart
import 'package:mockito/mockito.dart';
import 'package:mockito/annotations.dart';

@GenerateMocks([UserRepository])
void main() {
  late MockUserRepository mockRepository;
  late UserService service;

  setUp(() {
    mockRepository = MockUserRepository();
    service = UserService(mockRepository);
  });

  test('fetches user by id', () async {
    final user = User(id: 1, name: 'John');
    when(mockRepository.findById(1)).thenAnswer((_) async => user);

    final result = await service.getUser(1);

    expect(result, equals(user));
    verify(mockRepository.findById(1)).called(1);
  });
}
```

## Common Patterns

### Factory Constructors

```dart
class User {
  final int id;
  final String name;
  final String email;

  const User({
    required this.id,
    required this.name,
    required this.email,
  });

  // Factory from JSON
  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'] as int,
      name: json['name'] as String,
      email: json['email'] as String,
    );
  }

  // Factory for default user
  factory User.guest() {
    return const User(
      id: 0,
      name: 'Guest',
      email: 'guest@example.com',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'email': email,
    };
  }
}
```

### Extension Methods

```dart
extension StringExtensions on String {
  String capitalize() {
    if (isEmpty) return this;
    return '${this[0].toUpperCase()}${substring(1)}';
  }

  bool get isValidEmail {
    return RegExp(r'^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$').hasMatch(this);
  }
}

extension DateTimeExtensions on DateTime {
  String get formatted => '${day.toString().padLeft(2, '0')}/'
      '${month.toString().padLeft(2, '0')}/$year';

  bool get isToday {
    final now = DateTime.now();
    return year == now.year && month == now.month && day == now.day;
  }
}

// Usage
final name = 'john'.capitalize(); // 'John'
final isValid = 'test@example.com'.isValidEmail; // true
```

### Sealed Classes (Dart 3)

```dart
sealed class Result<T> {}

class Success<T> extends Result<T> {
  final T data;
  Success(this.data);
}

class Error<T> extends Result<T> {
  final String message;
  Error(this.message);
}

class Loading<T> extends Result<T> {}

// Usage with exhaustive pattern matching
Widget buildResult(Result<User> result) {
  return switch (result) {
    Success(data: final user) => Text(user.name),
    Error(message: final msg) => Text('Error: $msg'),
    Loading() => const CircularProgressIndicator(),
  };
}
```

### Freezed for Immutable Data

```dart
import 'package:freezed_annotation/freezed_annotation.dart';

part 'user.freezed.dart';
part 'user.g.dart';

@freezed
class User with _$User {
  const factory User({
    required int id,
    required String name,
    required String email,
    @Default(false) bool isActive,
  }) = _User;

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
}

// Usage
final user = User(id: 1, name: 'John', email: 'john@example.com');
final updatedUser = user.copyWith(name: 'Jane');
```

## Project Structure

### Feature-Based Organization

```
lib/
├── main.dart
├── app.dart
├── core/
│   ├── constants/
│   ├── extensions/
│   ├── utils/
│   └── widgets/
├── features/
│   ├── auth/
│   │   ├── data/
│   │   ├── domain/
│   │   └── presentation/
│   ├── home/
│   │   ├── data/
│   │   ├── domain/
│   │   └── presentation/
│   └── profile/
└── shared/
    ├── models/
    ├── services/
    └── widgets/
```

### Naming Conventions

```dart
// Files: snake_case
// user_repository.dart
// home_screen.dart

// Classes: PascalCase
class UserRepository {}
class HomeScreen extends StatelessWidget {}

// Variables and functions: camelCase
final userName = 'John';
void fetchUserData() {}

// Constants: camelCase or SCREAMING_SNAKE_CASE
const defaultPadding = 16.0;
const API_BASE_URL = 'https://api.example.com';

// Private: underscore prefix
class _HomeScreenState extends State<HomeScreen> {}
final _internalCache = <String, dynamic>{};
```
