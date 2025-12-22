/*using Microsoft.AspNetCore.Mvc;

namespace CarPrice.ApiGateway.Controllers
{
    public class GrpcProxyController : Controller
    {
        public IActionResult Index()
        {
            return View();
        }
    }
}
*/



/*

using CarPrice.GRPCService;
using Grpc.Net.Client;
using Microsoft.AspNetCore.Mvc;
using System.Threading.Tasks;

namespace CarPrice.ApiGateway.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class GrpcProxyController : ControllerBase
    {
        // GET api/grpcproxy/brands
        [HttpGet("brands")]
        public async Task<IActionResult> GetBrands()
        {
            // gRPC server adresi (gRPC servisini çalıştırırken gördüğün port)
            var grpcAddress = "https://localhost:7006"; // <-- kendi gRPC server portunu buraya yaz

            // Create channel
            using var channel = GrpcChannel.ForAddress(grpcAddress);
            var client = new VehicleService.VehicleServiceClient(channel); // proto'dan üretilmiş client

            var reply = await client.GetBrandsAsync(new BrandRequest());
            // reply.Brands -> repeated string
            return Ok(reply.Brands);
        }
    }
}
*/


using CarPrice.GRPCService;
using Grpc.Net.Client;
using Microsoft.AspNetCore.Mvc;
using System.Threading.Tasks;



namespace CarPrice.ApiGateway.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class GrpcProxyController : ControllerBase
    {

        //REST ISTEGINIGRPC YE CEVIREN BIR KOPRU GOREVI GORUYOR
        [HttpGet("brands")]
        public async Task<IActionResult> GetBrands()
        {
            var grpcAddress = "https://localhost:7006";

            using var channel = GrpcChannel.ForAddress(grpcAddress);
            var client = new VehicleService.VehicleServiceClient(channel);

            var reply = await client.GetBrandsAsync(new BrandRequest());

            return Ok(reply.Brands);
        }
    }
}
