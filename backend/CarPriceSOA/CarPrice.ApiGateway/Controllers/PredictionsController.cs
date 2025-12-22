using Microsoft.AspNetCore.Mvc;
using CarPrice.DataAccess.Repositories;

namespace CarPrice.ApiGateway.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class PredictionsController : ControllerBase
    {
        private readonly PredictionRepository _repo;

        public PredictionsController()
        {
            _repo = new PredictionRepository();
        }

        // POST: https://localhost:7188/api/Predictions/save
        [HttpPost("save")]
        public IActionResult Save([FromBody] PricePredictionInsertDto dto)
        {
            if (dto == null) return BadRequest("Body boş.");

            if (dto.UserId <= 0) return BadRequest("UserId gerekli.");
            if (dto.PredictedPrice <= 0) return BadRequest("PredictedPrice gerekli.");

            _repo.InsertPrediction(dto);
            return Ok(new { message = "Tahmin kaydedildi." });
        }

        // GET: https://localhost:7188/api/Predictions/my/1
        [HttpGet("my/{userId}")]
        public IActionResult My(int userId)
        {
            if (userId <= 0) return BadRequest("UserId gerekli.");

            var list = _repo.GetPredictionsByUserId(userId);
            return Ok(list);
        }
    }
}