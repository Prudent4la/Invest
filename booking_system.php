<?php
require 'db.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $name = $_POST['name'];
    $email = $_POST['email'];
    $phone = $_POST['phone'];
    $service = $_POST['service_name'];
    $date = $_POST['booking_date'];
    $time = $_POST['booking_time'];

    try {
        $pdo->beginTransaction();

        // 1. Check if user already exists by email
        $stmt = $pdo->prepare("SELECT id FROM users WHERE email = ?");
        $stmt->execute([$email]);
        $user = $stmt->fetch();

        if (!$user) {
            // Insert new user including the phone number
            $stmt = $pdo->prepare("INSERT INTO users (name, email, phone) VALUES (?, ?, ?)");
            $stmt->execute([$name, $email, $phone]);
            $userId = $pdo->lastInsertId();
        } else {
            $userId = $user['id'];
        }

        // 2. Insert the booking linked to the user
        $stmt = $pdo->prepare("INSERT INTO bookings (user_id, service_name, booking_date, booking_time) VALUES (?, ?, ?, ?)");
        $stmt->execute([$userId, $service, $date, $time]);

        $pdo->commit();
        echo "Booking successfully created!";
    } catch (Exception $e) {
        $pdo->rollBack();
        echo "Error: " . $e->getMessage();
    }
}
?>