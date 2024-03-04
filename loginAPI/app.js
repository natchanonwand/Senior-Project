const express = require('express');
const cors = require('cors');
const mysql = require('mysql2/promise');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');

const app = express();
const port = 3333;

// Secret key for JWT
const secret = 'Fullstack-login-project';

// Enable CORS
app.use(cors());
// Parse JSON bodies
app.use(express.json());

// Create connection pool
const pool = mysql.createPool({
  host: 'localhost',
  user: 'root',
  password: 'MYSQL_ROOT_PASSWORD',
  port: 9906,
  database: 'user'
});

// GET endpoint to fetch all users
app.get('/register', async (req, res) => {
  try {
    const connection = await pool.getConnection();
    const [rows] = await connection.query('SELECT * FROM users');
    connection.release();

    res.json(rows);
  } catch (error) {
    console.error('Error fetching users:', error);
    res.status(500).json({ error: 'Error fetching users' });
  }
});

// Registration endpoint
app.post('/register', async (req, res) => {
  const { email, password, fname, lname } = req.body;

  try {
    // Hash the password
    const hashedPassword = await bcrypt.hash(password, 10);

    // Insert the user data with hashed password into the database
    const connection = await pool.getConnection();
    const insertQuery = 'INSERT INTO users (email, password, fname, lname) VALUES (?, ?, ?, ?)';
    await connection.query(insertQuery, [email, hashedPassword, fname, lname]);
    connection.release();

    res.status(201).json({ message: 'User registered successfully' });
  } catch (error) {
    console.error('Error registering user:', error);
    res.status(500).json({ error: 'Error registering user' });
  }
});

// Login endpoint
app.post('/login', async (req, res) => {
  const { email, password } = req.body;

  try {
    // Query the database to find the user with the provided email
    const connection = await pool.getConnection();
    const [rows] = await connection.query('SELECT * FROM users WHERE email = ?', [email]);
    connection.release();

    // If no user found with the provided email, return an error
    if (rows.length === 0) {
      return res.status(401).json({ error: 'Invalid email or password' });
    }

    const user = rows[0]; //create array

    // Compare the provided password with the hashed password from the database
    const passwordMatch = await bcrypt.compare(password, user.password);

    // If passwords match, generate a JWT token and send it in the response
    if (passwordMatch) {
      const token = jwt.sign({ email: user.email}, secret, { expiresIn: '1h' });
      return res.json({status:'ok',message:'login success', token });
    } else {
      return res.status(401).json({ status:'error',message:'login failed' });
    }
  } catch (error) {
    console.error('Error logging in:', error);
    return res.status(500).json({ error: 'Error logging in' });
  }
});

app.post('/authen', async (req, res) =>{
  try{
    const token = req.headers.authorization.split(' ')[1]
    var decoded = jwt.verify(token, secret);
    res.json({ status:'ok', decoded })
  } catch(err){
    res.json({ status:'error', message: err.message })
  }
  
})

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
