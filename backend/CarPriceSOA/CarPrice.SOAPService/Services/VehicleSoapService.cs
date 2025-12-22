

using CarPrice.Business.Interfaces;

namespace CarPrice.SOAPService.Services
{
    public class VehicleSoapService : IVehicleSoapService
    {
        private readonly ICarService _carService;

        public VehicleSoapService(ICarService carService)
        {
            _carService = carService;
        }

        /* public string GetBrands()
         {
             var brands = _carService.GetBrands();
             return string.Join(",", brands);

         }*/

        public string GetBrands()
        {
            return "BMW, Audi, Mercedes, Toyota, Renault";
        }

    }
}
