using Microsoft.AspNetCore.Mvc;
using CarPrice.DataAccess.Repositories;

namespace CarPrice.ApiGateway.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class LookupController : ControllerBase
    {
        private readonly LookupRepository _repo;

        public LookupController()
        {
            _repo = new LookupRepository();
        }

        [HttpGet("brands")]
        public IActionResult GetBrands()
            => Ok(_repo.GetBrands());

        [HttpGet("models")]
        public IActionResult GetModels(int brandId)
            => Ok(_repo.GetModelsByBrand(brandId));

        [HttpGet("fueltypes")]
        public IActionResult GetFuelTypes()
            => Ok(_repo.GetFuelTypes());

        [HttpGet("geartypes")]
        public IActionResult GetGearTypes()
            => Ok(_repo.GetGearTypes());

        [HttpGet("colors")]
        public IActionResult GetColors()
            => Ok(_repo.GetColors());

        [HttpGet("bodytypes")]
        public IActionResult GetBodyTypes()
            => Ok(_repo.GetBodyTypes());
    }
}