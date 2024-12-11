<?php

// Розбиття тимчасової змінної
// Код до рефакторингу

function calculateFinalPrice($basePrice, $taxRate, $discountRate, $shippingFee) {
    if ($basePrice < 0 || $taxRate < 0 || $taxRate > 1 || $discountRate < 0 || $discountRate > 1 || $shippingFee < 0) {
        throw new InvalidArgumentException("Некоректні вхідні дані.");
    }

    $temp = $basePrice;

    // Крок 1: Розрахунок ціни з податком
    $temp += $temp * $taxRate;

    // Крок 2: Розрахунок ціни зі знижкою
    if ($discountRate > 0) {
        $temp -= $temp * $discountRate;
    }

    // Крок 3: Додавання вартості доставки
    $temp += $shippingFee;

    return $temp;
}

function generateInvoice($basePrice, $taxRate, $discountRate, $shippingFee) {
    echo "=== Інвойс ===\n";
    echo "Базова ціна: $" . number_format($basePrice, 2) . "\n";

    $temp = $basePrice;

    // Крок 1: Розрахунок ціни з податком
    $temp += $temp * $taxRate;
    echo "Ціна з податком: $" . number_format($temp, 2) . " (Податкова ставка: " . ($taxRate * 100) . "%)\n";

    // Крок 2: Розрахунок ціни зі знижкою
    if ($discountRate > 0) {
        $temp -= $temp * $discountRate;
        echo "Ціна зі знижкою: $" . number_format($temp, 2) . " (Знижка: " . ($discountRate * 100) . "%)\n";
    } else {
        echo "Знижка не застосована.\n";
    }

    // Крок 3: Додавання вартості доставки
    $temp += $shippingFee;
    echo "Вартість доставки: $" . number_format($shippingFee, 2) . "\n";

    echo "Кінцева ціна: $" . number_format($temp, 2) . "\n";
    echo "=================\n";
}

// Приклад використання
try {
    $basePrice = 100.00; // Базова ціна товару
    $taxRate = 0.2; // Податкова ставка (20%)
    $discountRate = 0.1; // Знижка (10%)
    $shippingFee = 15.00; // Вартість доставки

    // Розрахунок фінальної ціни
    $finalPrice = calculateFinalPrice($basePrice, $taxRate, $discountRate, $shippingFee);
    echo "Кінцева ціна: $" . number_format($finalPrice, 2) . "\n";

    // Генерація інвойсу
    generateInvoice($basePrice, $taxRate, $discountRate, $shippingFee);

} catch (InvalidArgumentException $e) {
    echo "Помилка: " . $e->getMessage() . "\n";
}

// Код після рефакторингу

function calculateFinalPriceRefactored($basePrice, $taxRate, $discountRate, $shippingFee) {
    if ($basePrice < 0 || $taxRate < 0 || $taxRate > 1 || $discountRate < 0 || $discountRate > 1 || $shippingFee < 0) {
        throw new InvalidArgumentException("Некоректні вхідні дані.");
    }

    // Крок 1: Розрахунок ціни з податком
    $priceWithTax = $basePrice + ($basePrice * $taxRate);

    // Крок 2: Розрахунок ціни зі знижкою
    $priceWithDiscount = ($discountRate > 0) ? $priceWithTax - ($priceWithTax * $discountRate) : $priceWithTax;

    // Крок 3: Додавання вартості доставки
    $finalPrice = $priceWithDiscount + $shippingFee;

    return $finalPrice;
}

function generateInvoiceRefactored($basePrice, $taxRate, $discountRate, $shippingFee) {
    echo "=== Інвойс ===\n";
    echo "Базова ціна: $" . number_format($basePrice, 2) . "\n";

    // Крок 1: Розрахунок ціни з податком
    $priceWithTax = $basePrice + ($basePrice * $taxRate);
    echo "Ціна з податком: $" . number_format($priceWithTax, 2) . " (Податкова ставка: " . ($taxRate * 100) . "%)\n";

    // Крок 2: Розрахунок ціни зі знижкою
    $priceWithDiscount = ($discountRate > 0) ? $priceWithTax - ($priceWithTax * $discountRate) : $priceWithTax;
    if ($discountRate > 0) {
        echo "Ціна зі знижкою: $" . number_format($priceWithDiscount, 2) . " (Знижка: " . ($discountRate * 100) . "%)\n";
    } else {
        echo "Знижка не застосована.\n";
    }

    // Крок 3: Додавання вартості доставки
    echo "Вартість доставки: $" . number_format($shippingFee, 2) . "\n";

    $finalPrice = $priceWithDiscount + $shippingFee;
    echo "Кінцева ціна: $" . number_format($finalPrice, 2) . "\n";
    echo "=================\n";
}

// Приклад використання
try {
    $basePrice = 100.00; // Базова ціна товару
    $taxRate = 0.2; // Податкова ставка (20%)
    $discountRate = 0.1; // Знижка (10%)
    $shippingFee = 15.00; // Вартість доставки

    // Розрахунок фінальної ціни
    $finalPrice = calculateFinalPriceRefactored($basePrice, $taxRate, $discountRate, $shippingFee);
    echo "Кінцева ціна: $" . number_format($finalPrice, 2) . "\n";

    // Генерація інвойсу
    generateInvoiceRefactored($basePrice, $taxRate, $discountRate, $shippingFee);

} catch (InvalidArgumentException $e) {
    echo "Помилка: " . $e->getMessage() . "\n";
}






// Замінити цикл на рекурсію
// Код до рефакторингу

function getSubgroups($pdo, $groupId) {
    $subgroups = [];
    $queue = [$groupId];

    while (!empty($queue)) {
        $currentId = array_shift($queue);

        // Виконання запиту для отримання підгруп
        $stmt = $pdo->prepare("SELECT id FROM groups WHERE parent_id = ?");
        $stmt->execute([$currentId]);
        $results = $stmt->fetchAll(PDO::FETCH_ASSOC);

        foreach ($results as $row) {
            $subgroups[] = $row['id'];
            $queue[] = $row['id']; // Додаємо підгрупу до черги для подальшої обробки
        }
    }

    return $subgroups;
}

// Код після рефакторингу

function getSubgroupsRecursive($pdo, $groupId, &$subgroups = []) {
    // Виконання запиту для отримання підгруп
    $stmt = $pdo->prepare("SELECT id FROM groups WHERE parent_id = ?");
    $stmt->execute([$groupId]);
    $results = $stmt->fetchAll(PDO::FETCH_ASSOC);

    foreach ($results as $row) {
        $subgroups[] = $row['id']; // Додаємо підгрупу до списку
        getSubgroupsRecursive($pdo, $row['id'], $subgroups); // Рекурсивно обробляємо підгрупу
    }

    return $subgroups;
}






// Замінити значення на об’єкт
// Код до рефакторингу

// Маршрут для обробки замовлення
$app->post('/order/{id}/update-status', function ($request, $response, $args) {
    $orderId = $args['id'];
    $newStatus = $request->getParsedBody()['status'];

    // Модель для отримання замовлення
    $order = OrderModel::find($orderId);
    if (!$order) {
        return $response->withStatus(404)->write("Замовлення не знайдено");
    }

    // Перевірка статусу
    $currentStatus = $order->status;
    if (($currentStatus === "delivered" && $newStatus !== "returned") ||
        $currentStatus === "canceled") {
        return $response->withStatus(400)->write("Зміна статусу неможлива");
    }

    // Оновлення статусу
    $order->status = $newStatus;
    $order->save();

    return $response->withJson(["message" => "Статус оновлено"]);
});

// Код після рефакторингу

class OrderStatus {
    private string $status;
    private const VALID_STATUSES = [
        'pending',
        'shipped',
        'delivered',
        'returned',
        'canceled',
    ];

    public function __construct(string $status) {
        if (!in_array($status, self::VALID_STATUSES, true)) {
            throw new InvalidArgumentException("Недійсний статус: $status");
        }
        $this->status = $status;
    }

    public function isChangeAllowed(OrderStatus $newStatus): bool {
        if ($this->status === 'delivered' && $newStatus->getStatus() !== 'returned') {
            return false;
        }
        if ($this->status === 'canceled') {
            return false;
        }
        return true;
    }

    public function getStatus(): string {
        return $this->status;
    }
}

// Маршрут для обробки замовлення
$app->post('/order/{id}/update-status', function ($request, $response, $args) {
    $orderId = $args['id'];
    $newStatus = $request->getParsedBody()['status'];

    // Модель для отримання замовлення
    $order = OrderModel::find($orderId);
    if (!$order) {
        return $response->withStatus(404)->write("Замовлення не знайдено");
    }

    // Поточний статус як об'єкт
    $currentStatus = new OrderStatus($order->status);
    $newStatusObject = new OrderStatus($newStatus);

    // Перевірка статусу
    if (!$currentStatus->isChangeAllowed($newStatusObject)) {
        return $response->withStatus(400)->write("Зміна статусу неможлива");
    }

    // Оновлення статусу
    $order->status = $newStatusObject->getStatus();
    $order->save();

    return $response->withJson(["message" => "Статус оновлено"]);
});

?>
