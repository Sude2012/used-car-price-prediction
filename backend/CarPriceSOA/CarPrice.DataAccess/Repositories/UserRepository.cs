/*
using CarPrice.Core.DTOs;
using CarPrice.Core.Entities;
using Microsoft.Data.SqlClient;
using System;
using System.Security.Cryptography;
using System.Text;


namespace CarPrice.DataAccess.Repositories
{
    public class UserRepository : IUserRepository
    {
        private readonly string _connectionString =
            "Server=DESKTOP-BBBCJ3C\\SQLEXPRESS;Database=projeOrnek;Trusted_Connection=True;TrustServerCertificate=True;";

        // ---------------------------------------------------
        // REGISTER (Yeni kullanıcı ekler)
        // ---------------------------------------------------
        public bool Register(RegisterDTO dto)
        {
            var hash = HashPassword(dto.Password);

            using (SqlConnection conn = new SqlConnection(_connectionString))
            {
                conn.Open();

                string query = @"
                    INSERT INTO Users (FirstName, LastName, Email, PasswordHash, Role, CreatedAt)
                    VALUES (@FirstName, @LastName, @Email, @PasswordHash, 'User', GETDATE())
                ";

                SqlCommand cmd = new SqlCommand(query, conn);
                cmd.Parameters.AddWithValue("@FirstName", dto.FirstName);
                cmd.Parameters.AddWithValue("@LastName", dto.LastName);
                cmd.Parameters.AddWithValue("@Email", dto.Email);
                cmd.Parameters.AddWithValue("@PasswordHash", hash);

                return cmd.ExecuteNonQuery() > 0;
            }
        }

        // ---------------------------------------------------
        // LOGIN (E-posta ve şifreyi doğrular)
        // ---------------------------------------------------
        public User Login(LoginDTO dto)
        {
            using (SqlConnection conn = new SqlConnection(_connectionString))
            {
                conn.Open();

                string query = @"SELECT * FROM Users WHERE Email = @Email";

                SqlCommand cmd = new SqlCommand(query, conn);
                cmd.Parameters.AddWithValue("@Email", dto.Email);

                SqlDataReader reader = cmd.ExecuteReader();

                if (reader.Read())
                {
                    string storedHash = reader["PasswordHash"].ToString();

                    if (VerifyPassword(dto.Password, storedHash))
                    {
                        return new User
                        {
                            UserId = (int)reader["UserId"],
                            FirstName = reader["FirstName"].ToString(),
                            LastName = reader["LastName"].ToString(),
                            Email = reader["Email"].ToString(),
                            Role = reader["Role"].ToString(),
                            CreatedAt = (DateTime)reader["CreatedAt"]
                        };
                    }
                }
            }

            return null;
        }

        // ---------------------------------------------------
        // EMAIL İLE KULLANICI GETİRME
        // ---------------------------------------------------
        public User GetByEmail(string email)
        {
            using (SqlConnection conn = new SqlConnection(_connectionString))
            {
                conn.Open();
                string query = @"SELECT * FROM Users WHERE Email = @Email";

                SqlCommand cmd = new SqlCommand(query, conn);
                cmd.Parameters.AddWithValue("@Email", email);

                SqlDataReader reader = cmd.ExecuteReader();

                if (reader.Read())
                {
                    return new User
                    {
                        UserId = (int)reader["UserId"],
                        FirstName = reader["FirstName"].ToString(),
                        LastName = reader["LastName"].ToString(),
                        Email = reader["Email"].ToString(),
                        Role = reader["Role"].ToString(),
                        CreatedAt = (DateTime)reader["CreatedAt"]
                    };
                }
            }

            return null;
        }

        // ---------------------------------------------------
        // PASSWORD HASH METHOD
        // ---------------------------------------------------
        private string HashPassword(string password)
        {
            using (SHA256 sha = SHA256.Create())
            {
                byte[] bytes = sha.ComputeHash(Encoding.UTF8.GetBytes(password));
                return Convert.ToBase64String(bytes);
            }
        }

        // ---------------------------------------------------
        // PASSWORD VERIFY METHOD
        // ---------------------------------------------------
        private bool VerifyPassword(string password, string storedHash)
        {
            string hash = HashPassword(password);
            return hash == storedHash;
        }
    }
}
*/



using CarPrice.Core.DTOs;
using CarPrice.Core.Entities;
using Microsoft.Data.SqlClient;
using System;
using System.Security.Cryptography;
using System.Text;

namespace CarPrice.DataAccess.Repositories
{
    public class UserRepository : IUserRepository
    {

        private readonly string _connectionString =
       "Server=localhost\\SQLEXPRESS01;Database=CarPriceDB;Trusted_Connection=True;TrustServerCertificate=True;";

        // ---------------------------------------------------
        // REGISTER (Yeni kullanıcı ekler)
        // ---------------------------------------------------
        public bool Register(RegisterDTO dto)
        {
            try
            {
                var hash = HashPassword(dto.Password);

                using (SqlConnection conn = new SqlConnection(_connectionString))
                {
                    conn.Open();

                    string query = @"
                        INSERT INTO Users (FirstName, LastName, Email, PasswordHash, Role, CreatedAt)
                        VALUES (@FirstName, @LastName, @Email, @PasswordHash, 'User', GETDATE())
                    ";

                    SqlCommand cmd = new SqlCommand(query, conn);
                    cmd.Parameters.AddWithValue("@FirstName", dto.FirstName);
                    cmd.Parameters.AddWithValue("@LastName", dto.LastName);
                    cmd.Parameters.AddWithValue("@Email", dto.Email);
                    cmd.Parameters.AddWithValue("@PasswordHash", hash);

                    return cmd.ExecuteNonQuery() > 0;
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine("SQL REGISTER ERROR → " + ex.Message);
                return false;
            }
        }

        // ---------------------------------------------------
        // LOGIN (E-posta ve şifreyi doğrular)
        // ---------------------------------------------------
        public User Login(LoginDTO dto)
        {
            try
            {
                using (SqlConnection conn = new SqlConnection(_connectionString))
                {
                    conn.Open();

                    string query = @"SELECT * FROM Users WHERE Email = @Email";

                    SqlCommand cmd = new SqlCommand(query, conn);
                    cmd.Parameters.AddWithValue("@Email", dto.Email);

                    SqlDataReader reader = cmd.ExecuteReader();

                    if (reader.Read())
                    {
                        string storedHash = reader["PasswordHash"].ToString();

                        if (VerifyPassword(dto.Password, storedHash))
                        {
                            return new User
                            {
                                UserId = (int)reader["UserId"],
                                FirstName = reader["FirstName"].ToString(),
                                LastName = reader["LastName"].ToString(),
                                Email = reader["Email"].ToString(),
                                Role = reader["Role"].ToString(),
                                CreatedAt = (DateTime)reader["CreatedAt"]
                            };
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine("SQL LOGIN ERROR → " + ex.Message);
            }

            return null;
        }

        // ---------------------------------------------------
        // EMAIL İLE KULLANICI GETİRME
        // ---------------------------------------------------
        public User GetByEmail(string email)
        {
            try
            {
                using (SqlConnection conn = new SqlConnection(_connectionString))
                {
                    conn.Open();
                    string query = @"SELECT * FROM Users WHERE Email = @Email";

                    SqlCommand cmd = new SqlCommand(query, conn);
                    cmd.Parameters.AddWithValue("@Email", email);

                    SqlDataReader reader = cmd.ExecuteReader();

                    if (reader.Read())
                    {
                        return new User
                        {
                            UserId = (int)reader["UserId"],
                            FirstName = reader["FirstName"].ToString(),
                            LastName = reader["LastName"].ToString(),
                            Email = reader["Email"].ToString(),
                            Role = reader["Role"].ToString(),
                            CreatedAt = (DateTime)reader["CreatedAt"]
                        };
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine("SQL GetByEmail ERROR → " + ex.Message);
            }

            return null;
        }

        // ---------------------------------------------------
        // PASSWORD HASH METHOD
        // ---------------------------------------------------
        private string HashPassword(string password)
        {
            using (SHA256 sha = SHA256.Create())
            {
                byte[] bytes = sha.ComputeHash(Encoding.UTF8.GetBytes(password));
                return Convert.ToBase64String(bytes);
            }
        }

        // ---------------------------------------------------
        // PASSWORD VERIFY METHOD
        // ---------------------------------------------------
        private bool VerifyPassword(string password, string storedHash)
        {
            string hash = HashPassword(password);
            return hash == storedHash;
        }
    }
}