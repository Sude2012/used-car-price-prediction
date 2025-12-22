
using CarPrice.Business.Interfaces;
using Microsoft.AspNetCore.Mvc;
// using CarPrice.Business.Concrete; // 👈 Bu satıra artık gerek yok

namespace CarPrice.ApiGateway.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class CarController : ControllerBase
    {
        private readonly ICarService _carService;

        // DÜZELTME: Constructor'a ICarService enjekte edilmeli
        public CarController(ICarService carService)
        {
            _carService = carService; // 👈 DI Konteyneri (Program.cs'te kaydettiğiniz) bu nesneyi verecek.
        }

        [HttpGet("brands")]
        public IActionResult GetBrands()
        {
            var result = _carService.GetBrands();
            return Ok(result);
        }
    }
}