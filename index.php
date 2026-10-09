<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bookings System</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 50px; background-color: #f4f4f9; }
        form { background: white; padding: 20px; border-radius: 8px; max-width: 400px; box-shadow: 0px 0px 10px rgba(0,0,0,0.1); }
        label { display: block; margin-top: 10px; font-weight: bold; }
        input, select { width: 100%; padding: 8px; margin-top: 5px; box-sizing: border-box; border: 1px solid #ccc; border-radius: 4px; }
        button { margin-top: 15px; width: 100%; background: #007bff; color: white; border: none; padding: 10px; border-radius: 4px; cursor: pointer; font-size: 16px; }
        button:hover { background: #0056b3; }
    </style>
</head>
<body>

    <h2>Create a New Booking</h2>

    <form action="process_booking.php" method="POST">
        <label>Full Name:</label>
        <input type="text" name="name" required>

        <label>Email:</label>
        <input type="email" name="email" required>

        <label>Phone Number:</label>
        <input type="tel" name="phone" required>
		
	  <label>Address:</label>
        <input type="Address" name="Address" required>

        <label>Service:</label>
        <input type="text" name="service_name" required>

        <label>Date:</label>
        <input type="date" name="booking_date" required>

        <label>Time:</label>
        <input type="time" name="booking_time" required>

        <button type="submit" name="submit_booking">Confirm Booking</button>
    </form>

</body>
</html>