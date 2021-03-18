<?php
    $host = "localhost";
    $username = "root";
    $password = "CS288hw8!";
    $database = "test_stonks";

    //$order_by = $_GET["order_by"];
    //$sorting = $_GET["sorting"];
    $order_by = '';
    $sorting = '';
    
    // Create a new connection
    $conn = new mysqli($host, $username, $password, $database);

    if ($conn->connect_error) {
        die("Connection Failed: " . $conn->connect_error);
    }

    // Did not know what table to load in so I just hardcoded it.
    $table_name = $argv[1];
    
    $sql = "SELECT * FROM $table_name";

    if ($order_by && $sorting) {
        $sql = "SELECT * FROM $table_name ORDER BY $order_by $sorting";
    }
    $result = $conn->query($sql);
    
    $conn->close();
?>

<h1>
    <?php echo $table_name ?>
</h1>

<table>
    <thead>
        <th><a>symbol</a></th>
        <th><a>name</a></th>
        <th><a>price</a></th>
        <th><a>chng</a></th>
        <th><a>p_change</a></th>
        <th><a>volume</a></th>
        <th><a>market_cap</a></th>
    </thead>
    <tbody>
        <?php
            if ($result->num_rows > 0) {
                // output data of each row
                while($row = $result->fetch_assoc()) {
                    echo "<tr><td>" . $row["symbol"]. "</td><td>" . $row["name"]. "</td><td>" . $row["price"] . "</td><td>" . $row["chng"] . "</td><td>" . $row["p_change"] . "</td><td>" . $row["volume"] . "</td><td>" . $row["market_cap"] . "</td></tr>";
                }
            } else {
                echo "0 results";
            }
        ?>
    </tbody>
</table>

<style>
    table, tr, td, th {
        border: 1px solid black;
    }
</style>
