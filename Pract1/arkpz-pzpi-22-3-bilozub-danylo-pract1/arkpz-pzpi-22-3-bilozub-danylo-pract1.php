<?php

// Оформлення  коду

// Поганий приклад

$conn = mysqli_connect("localhost", "root", "", "shop");
$res = mysqli_query($conn, "SELECT * FROM products");
while ($row = mysqli_fetch_assoc($res)) {
    echo $row['name'] . " - " . $row['price'] . "<br>";
}


// Гарний приклад

// Підключення до бази даних
$connection = new mysqli("localhost", "root", "", "shop");

// Перевірка підключення
if ($connection->connect_error) {
    die("Помилка з'єднання: " . $connection->connect_error);
}

// Запит до бази даних
$query = "SELECT name, price FROM products";
$result = $connection->query($query);

if ($result && $result->num_rows > 0) {
    // Виведення результатів
    while ($product = $result->fetch_assoc()) {
        echo "{$product['name']} - {$product['price']}<br>";
    }
} else {
    echo "Немає доступних товарів.";
}

$connection->close();




// Структура коду

// Поганий приклад

$conn = mysqli_connect("localhost", "root", "", "shop");
function gP() {
    global $conn;
    $res = mysqli_query($conn, "SELECT * FROM products");
    while ($r = mysqli_fetch_assoc($res)) {
        echo $r['name'] . "<br>";
    }
}
gP();


// Гарний приклад

require_once __DIR__ . '/../vendor/autoload.php';

use Database\DatabaseConnection;
use Repositories\ProductRepository;
use Services\ProductService;

// Підключення до бази даних
$databaseConnection = new DatabaseConnection("localhost", "root", "", "shop");

// Створення репозиторію для продуктів
$productRepository = new ProductRepository($databaseConnection->getConnection());

// Створення сервісу для роботи з продуктами
$productService = new ProductService($productRepository);

// Виведення продуктів
$productService->displayProducts();

// Закриття підключення до бази даних
$databaseConnection->closeConnection();




// Форматування коду

// Поганий приклад

function getAllProductsSortedByPrice1($conn){$query="SELECT * FROM products ORDER BY price ASC";
$result=$conn->query($query);
if(!$result){die("Error: ".$conn->error);}
else{$products=[];
while($row=$result->fetch_assoc()){$products[]=$row;}
    return $products;}}


// Гарний приклад

function getAllProductsSortedByPrice($conn) {
    // SQL-запит для отримання товарів, відсортованих за ціною
    $query = "SELECT * FROM products ORDER BY price ASC";
    
    // Виконання запиту
    $result = $conn->query($query);
    
    // Перевірка на помилки
    if (!$result) {
        die("Помилка запиту: " . $conn->error);
    }
    
    // Формування масиву з товарами
    $products = [];
    while ($row = $result->fetch_assoc()) {
        $products[] = $row;
    }
    
    return $products;
    }




// Іменування змінних, функцій, класів

// Поганий приклад

function calc($db, $m) {
    $q = "SELECT SUM(qty) AS total FROM sales WHERE MONTH(date) = $m";
    $res = $db->query($q);
    if ($res) {
        $r = $res->fetch_assoc();
        return $r['total'];
    } else {
        return 0;
    }
}


// Гарний приклад

function calculateTotalSalesForMonth(mysqli $connection): int {
    // Підготовлений SQL-запит для запобігання SQL-ін'єкціям
    $query = "SELECT SUM(quantity) AS total_quantity FROM sales WHERE MONTH(sale_date) = ?";
    $result = $connection->query($query);

    // Отримання результату
    $totalQuantity = 0;
    if ($result) {
        $row = $result->fetch_assoc();
        $totalQuantity = $row['total_quantity'] ?? 0;
    }

    return $totalQuantity;
}




// Коментарі

// Поганий приклад

// Підключення до бази даних зоомагазину
$connection = new mysqli("localhost", "root", "", "shop"); 
// Створення  нового підключення з параметрами бд

if ($connection->connect_error) { // Перевірка на виникнення помилки
    die("Помилка з'єднання: " . $connection->connect_error); // Реагування на помилку
}

// Отримання всіх товарів
$query = "SELECT name FROM products"; // SQL запит для  отримання товарів
$result = $connection->query($query); // Виконання SQL запиту для нашої бази даних

if ($result && $result->num_rows > 0) { // Перевірка наявності результату
    // Виведення назв товарів
    while ($product = $result->fetch_assoc()) { // Цикл для проходження по результату
        echo $product['name'] . "<br>"; // Вивід
    }
} else {
    echo "Товари не знайдено."; // Помилка
}

$connection->close(); // Закриття з'єднання


// Гарний приклад

// Підключення до бази даних зоомагазину
$connection = new mysqli("localhost", "root", "", "shop");

if ($connection->connect_error) {
    die("Помилка з'єднання: " . $connection->connect_error);
}

// Отримання всіх товарів
$query = "SELECT name FROM products";
$result = $connection->query($query);

if ($result && $result->num_rows > 0) {
    // Виведення назв товарів
    while ($product = $result->fetch_assoc()) {
        echo $product['name'] . "<br>";
    }
} else {
    echo "Товари не знайдено.";
}

$connection->close();




// Документування коду

// Поганий приклад

function addProduct1($name, $price, $category, $connection ) {
    $query = "INSERT INTO products (name, price, category) 
    VALUES ('$name', '$price', '$category')";
    $result = mysqli_query($connection, $query);
    return $result;
}


// Гарний приклад

/**
 * Додає новий товар до бази даних
 *
 * Ця функція приймає назву товару, ціну та категорію, а потім додає їх до бази даних.
 * Вона використовує SQL-запит для вставки нових даних в таблицю продуктів.
 * 
 * @param mysqli $connection Підключення до бази даних
 * @param string $name Назва товару
 * @param float $price Ціна товару
 * @param string $category Категорія товару (наприклад, "Корми для тварин")
 * 
 * @return bool Повертає true, якщо товар успішно додано, або false в разі помилки
 */
function addProduct($name, $price, $category, $connection) {
    $query = "INSERT INTO products (name, price, category) VALUES ('$name', '$price', '$category')";
    $result = mysqli_query($connection, $query);
    return $result;
}




// Конвенції стилю кодування для PHP

// Поганий приклад

function addSale1($productId,$quantity,$totalPrice, $connection){
$query="INSERT INTO sales (product_id, quantity, total_price) VALUES('$productId', '$quantity', '$totalPrice')";
mysqli_query($connection,$query);
}


// Гарний приклад

/**
 * Додає запис про продаж товару в базу даних.
 *
 * Ця функція приймає ідентифікатор товару, кількість проданого товару і загальну вартість,
 * а також підключення до бази даних, а потім додає цей запис у таблицю продажів.
 *
 * @param mysqli $connection Підключення до бази даних
 * @param int $productId Ідентифікатор товару
 * @param int $quantity Кількість проданого товару
 * @param float $totalPrice Загальна вартість проданого товару
 * @return bool Повертає true, якщо запис успішно додано, і false в разі помилки
 */
function addSale($connection, $productId, $quantity, $totalPrice)
{
    // Перевірка на валідність введених даних
    if ($quantity <= 0 || $totalPrice <= 0) {
        return false;  // Якщо кількість або ціна некоректні, повертаємо false
    }
    // Підготовка SQL-запиту
    $query = "INSERT INTO sales (product_id, quantity, total_price) VALUES (1, 2, 15)";
    // Підготовка запиту для захисту від SQL-ін'єкцій
    $stmt = mysqli_prepare($connection, $query);
    if (!$stmt) {
        error_log("Error preparing query: " . mysqli_error($connection));
        return false;  // Якщо не вдалося підготувати запит
    }
    // Прив'язуємо параметри до запиту
    mysqli_stmt_bind_param($stmt, "iid", $productId, $quantity, $totalPrice);
    // Виконуємо запит
    $result = mysqli_stmt_execute($stmt);
    // Перевіряємо на успішне виконання запиту
    if (!$result) {
        // Логування помилки
        error_log("Error executing query: " . mysqli_error($connection));
        return false;  // Повертаємо false в разі помилки
    }
    // Закриваємо підготовлений запит
    mysqli_stmt_close($stmt);
    return true;  // Повертаємо true, якщо продаж успішно додано
}




// Кодування на основі тестування

//  Приклад тестування

use PHPUnit\Framework\TestCase;

class PriceCalculatorTest extends TestCase
{
    public function testCalculateTotalPrice()
    {
        // Приклад масиву товарів, де кожен товар має ціну та кількість
        $items = [
            ['price' => 10.5, 'quantity' => 2], // 2 товару по 10.5
            ['price' => 20.0, 'quantity' => 3], // 3 товару по 20.0
            ['price' => 5.0, 'quantity' => 5],  // 5 товарів по 5.0
        ];

        // Ожидаємий результат
        $expected = 10.5 * 2 + 20.0 * 3 + 5.0 * 5; // 21 + 60 + 25 = 106

        // Перевіряємо, чи вірно працює функція
        $this->assertEquals($expected, calculateTotalPrice($items));
    }
}




// Управління помилками в PHP

// Поганий приклад

function getProductById1($id,$connection) {
    $query = "SELECT * FROM products WHERE id = $id";
    $result = mysqli_query($connection, $query);

    if (!$result) {
        echo "Помилка виконання запиту!";
    }

    return mysqli_fetch_assoc($result);
}
$product = getProductById(5,$connection);


// Гарний приклад

function getProductById($id,$connection) {
    // Перевірка валідності ідентифікатора
    if (!is_int($id) || $id <= 0) {
        throw new InvalidArgumentException("Неприпустимий ідентифікатор товару: $id");
    }
    // SQL-запит
    $query = "SELECT * FROM products WHERE id = ?";
    $stmt = mysqli_prepare($connection, $query);
    if (!$stmt) {
        throw new Exception("Не вдалося підготувати запит: " . mysqli_error($connection));
    }
    mysqli_stmt_bind_param($stmt, 'i', $id);
    mysqli_stmt_execute($stmt);
    $result = mysqli_stmt_get_result($stmt);
    if (!$result) {
        throw new Exception("Помилка виконання запиту: " . mysqli_error($connection));
    }
    $product = mysqli_fetch_assoc($result);
    // Перевірка, чи знайдено товар
    if (!$product) {
        throw new Exception("Товар з ідентифікатором $id не знайдено.");
    }
    return $product;
}
// Використання функції з обробкою помилок
try {
    $product = getProductById(5,$connection);
    echo "Назва товару: " . $product['name'];
} catch (InvalidArgumentException $e) {
    echo "Помилка вхідних даних: " . $e->getMessage();
} catch (Exception $e) {
    error_log($e->getMessage()); // Логування помилки
    echo "Сталася помилка, спробуйте пізніше.";
}

?>