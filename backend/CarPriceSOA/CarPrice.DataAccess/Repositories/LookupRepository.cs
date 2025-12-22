


using Microsoft.Data.SqlClient;
using Dapper;

namespace CarPrice.DataAccess.Repositories
{
    public class LookupRepository
    {
        private readonly string _cs =
            "Server=localhost\\SQLEXPRESS01;Database=CarPriceDB;Trusted_Connection=True;TrustServerCertificate=True;";

        public IEnumerable<object> GetBrands()
        {
            using var conn = new SqlConnection(_cs);
            return conn.Query(@"
                SELECT 
                    BrandId AS id, 
                    Name AS name 
                FROM Brands
                ORDER BY Name
            ");
        }

        public IEnumerable<object> GetModelsByBrand(int brandId)
        {
            using var conn = new SqlConnection(_cs);
            return conn.Query(@"
                SELECT 
                    ModelId   AS id, 
                    ModelName AS name
                FROM Models
                WHERE BrandId = @brandId
                ORDER BY ModelName
            ", new { brandId });
        }

        public IEnumerable<object> GetFuelTypes()
        {
            using var conn = new SqlConnection(_cs);
            return conn.Query(@"
                SELECT 
                    FuelTypeId AS id, 
                    Name       AS name 
                FROM FuelTypes
                ORDER BY Name
            ");
        }

        public IEnumerable<object> GetGearTypes()
        {
            using var conn = new SqlConnection(_cs);
            return conn.Query(@"
                SELECT 
                    GearTypeId AS id, 
                    Name       AS name 
                FROM GearTypes
                ORDER BY Name
            ");
        }

        public IEnumerable<object> GetColors()
        {
            using var conn = new SqlConnection(_cs);
            return conn.Query(@"
                SELECT 
                    ColorId AS id, 
                    Name    AS name 
                FROM Colors
                ORDER BY Name
            ");
        }

        public IEnumerable<object> GetBodyTypes()
        {
            using var conn = new SqlConnection(_cs);
            return conn.Query(@"
                SELECT 
                    BodyTypeId AS id, 
                    Name       AS name 
                FROM BodyTypes
                ORDER BY Name
            ");
        }
    }
}