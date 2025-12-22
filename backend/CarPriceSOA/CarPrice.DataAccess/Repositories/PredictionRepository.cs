using System;
using System.Collections.Generic;
using Microsoft.Data.SqlClient;


namespace CarPrice.DataAccess.Repositories
{
    public class PredictionRepository
    {
        private readonly string _connectionString =
            "Server=localhost\\SQLEXPRESS01;Database=CarPriceDB;Trusted_Connection=True;TrustServerCertificate=True;";

        public void InsertPrediction(PricePredictionInsertDto dto)
        {
            using var conn = new SqlConnection(_connectionString);
            conn.Open();

            var sql = @"
INSERT INTO dbo.PricePredictions
(
    CarId,
    PredictionDate,
    PredictedPrice,
    RealPrice,
    ModelName,
    UserId,
    CreatedAt,
    InputYear,
    InputKilometer,
    InputGearTypeId,
    InputFuelTypeId,
    InputBodyTypeId,
    InputColorId,
    InputBrandId,
    InputModelId
)
VALUES
(
    @CarId,
    GETDATE(),
    @PredictedPrice,
    NULL,
    @ModelName,
    @UserId,
    GETDATE(),
    @InputYear,
    @InputKilometer,
    @InputGearTypeId,
    @InputFuelTypeId,
    @InputBodyTypeId,
    @InputColorId,
    @InputBrandId,
    @InputModelId
);";

            using var cmd = new SqlCommand(sql, conn);

            cmd.Parameters.AddWithValue("@CarId", dto.CarId);
            cmd.Parameters.AddWithValue("@PredictedPrice", dto.PredictedPrice);
            cmd.Parameters.AddWithValue("@ModelName", (object?)dto.ModelName ?? DBNull.Value);
            cmd.Parameters.AddWithValue("@UserId", dto.UserId);

            cmd.Parameters.AddWithValue("@InputYear", (object?)dto.InputYear ?? DBNull.Value);
            cmd.Parameters.AddWithValue("@InputKilometer", (object?)dto.InputKilometer ?? DBNull.Value);
            cmd.Parameters.AddWithValue("@InputGearTypeId", (object?)dto.InputGearTypeId ?? DBNull.Value);
            cmd.Parameters.AddWithValue("@InputFuelTypeId", (object?)dto.InputFuelTypeId ?? DBNull.Value);
            cmd.Parameters.AddWithValue("@InputBodyTypeId", (object?)dto.InputBodyTypeId ?? DBNull.Value);
            cmd.Parameters.AddWithValue("@InputColorId", (object?)dto.InputColorId ?? DBNull.Value);
            cmd.Parameters.AddWithValue("@InputBrandId", (object?)dto.InputBrandId ?? DBNull.Value);
            cmd.Parameters.AddWithValue("@InputModelId", (object?)dto.InputModelId ?? DBNull.Value);

            cmd.ExecuteNonQuery();
        }

        public List<PricePredictionRowDto> GetPredictionsByUserId(int userId)
        {
            using var conn = new SqlConnection(_connectionString);
            conn.Open();

            var sql = @"
SELECT TOP 100
    PredictionId,
    CarId,
    PredictionDate,
    PredictedPrice,
    RealPrice,
    ModelName,
    UserId,
    CreatedAt,
    InputYear,
    InputKilometer,
    InputGearTypeId,
    InputFuelTypeId,
    InputBodyTypeId,
    InputColorId,
    InputBrandId,
    InputModelId
FROM dbo.PricePredictions
WHERE UserId = @UserId
ORDER BY CreatedAt DESC;";

            using var cmd = new SqlCommand(sql, conn);
            cmd.Parameters.AddWithValue("@UserId", userId);

            using var reader = cmd.ExecuteReader();

            var list = new List<PricePredictionRowDto>();
            while (reader.Read())
            {
                list.Add(new PricePredictionRowDto
                {
                    PredictionId = reader.GetInt32(reader.GetOrdinal("PredictionId")),
                    CarId = reader.GetInt32(reader.GetOrdinal("CarId")),
                    PredictionDate = reader.GetDateTime(reader.GetOrdinal("PredictionDate")),
                    PredictedPrice = reader.GetDecimal(reader.GetOrdinal("PredictedPrice")),
                    ModelName = reader.IsDBNull(reader.GetOrdinal("ModelName")) ? null : reader.GetString(reader.GetOrdinal("ModelName")),
                    UserId = reader.GetInt32(reader.GetOrdinal("UserId")),
                    CreatedAt = reader.GetDateTime(reader.GetOrdinal("CreatedAt")),
                    InputYear = reader.IsDBNull(reader.GetOrdinal("InputYear")) ? (int?)null : reader.GetInt32(reader.GetOrdinal("InputYear")),
                    InputKilometer = reader.IsDBNull(reader.GetOrdinal("InputKilometer")) ? (int?)null : reader.GetInt32(reader.GetOrdinal("InputKilometer")),
                    InputGearTypeId = reader.IsDBNull(reader.GetOrdinal("InputGearTypeId")) ? (int?)null : reader.GetInt32(reader.GetOrdinal("InputGearTypeId")),
                    InputFuelTypeId = reader.IsDBNull(reader.GetOrdinal("InputFuelTypeId")) ? (int?)null : reader.GetInt32(reader.GetOrdinal("InputFuelTypeId")),
                    InputBodyTypeId = reader.IsDBNull(reader.GetOrdinal("InputBodyTypeId")) ? (int?)null : reader.GetInt32(reader.GetOrdinal("InputBodyTypeId")),
                    InputColorId = reader.IsDBNull(reader.GetOrdinal("InputColorId")) ? (int?)null : reader.GetInt32(reader.GetOrdinal("InputColorId")),
                    InputBrandId = reader.IsDBNull(reader.GetOrdinal("InputBrandId")) ? (int?)null : reader.GetInt32(reader.GetOrdinal("InputBrandId")),
                    InputModelId = reader.IsDBNull(reader.GetOrdinal("InputModelId")) ? (int?)null : reader.GetInt32(reader.GetOrdinal("InputModelId")),
                });
            }

            return list;
        }
    }

    // ✅ Insert için DTO
    public class PricePredictionInsertDto
    {
        public int UserId { get; set; }
        public int CarId { get; set; } = 2; // senin tabloda testte CarId=2 vardı, default verdim
        public decimal PredictedPrice { get; set; }
        public string? ModelName { get; set; }

        public int? InputYear { get; set; }
        public int? InputKilometer { get; set; }
        public int? InputGearTypeId { get; set; }
        public int? InputFuelTypeId { get; set; }
        public int? InputBodyTypeId { get; set; }
        public int? InputColorId { get; set; }
        public int? InputBrandId { get; set; }
        public int? InputModelId { get; set; }
    }

    // ✅ Listelemek için DTO
    public class PricePredictionRowDto
    {
        public int PredictionId { get; set; }
        public int CarId { get; set; }
        public DateTime PredictionDate { get; set; }
        public decimal PredictedPrice { get; set; }
        public string? ModelName { get; set; }
        public int UserId { get; set; }
        public DateTime CreatedAt { get; set; }

        public int? InputYear { get; set; }
        public int? InputKilometer { get; set; }
        public int? InputGearTypeId { get; set; }
        public int? InputFuelTypeId { get; set; }
        public int? InputBodyTypeId { get; set; }
        public int? InputColorId { get; set; }
        public int? InputBrandId { get; set; }
        public int? InputModelId { get; set; }
    }
}