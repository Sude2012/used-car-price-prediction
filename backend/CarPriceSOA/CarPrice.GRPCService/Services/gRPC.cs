/*using CarPrice.GRPCService;
using Grpc.Core;

namespace CarPrice.GRPCService.Services
{
    public class gRPC : gRPC.GreeterBase
    {
        private readonly ILogger<gRPC> _logger;
        public gRPC(ILogger<gRPC> logger)
        {
            _logger = logger;
        }

        public override Task<BrandResponse> SayHello(BrandRequest request, ServerCallContext context)
        {
            return Task.FromResult(new BrandResponse
            {
                Message = "Hello " + request.Name
            });
        }
    }
}
*/






/*
using CarPrice.GRPCService;
using Grpc.Core;

namespace CarPrice.GRPCService.Services
{
    public class gRPCService : VehicleService.VehicleServiceBase
    {
        private readonly ILogger<gRPCService> _logger;

        public gRPCService(ILogger<gRPCService> logger)
        {
            _logger = logger;
        }

        public override Task<BrandResponse> GetBrands(BrandRequest request, ServerCallContext context)
        {
            return Task.FromResult(new BrandResponse
            {
                Brands = "Hello " + request.
            });
        }
    }
}




*/



using CarPrice.GRPCService;
using Grpc.Core;

namespace CarPrice.GRPCService.Services
{
    public class gRPCService : VehicleService.VehicleServiceBase
    {
        private readonly ILogger<gRPCService> _logger;

        public gRPCService(ILogger<gRPCService> logger)
        {
            _logger = logger;
        }

        // Override edilen metod
        public override Task<BrandResponse> GetBrands(BrandRequest request, ServerCallContext context)
        {
            var response = new BrandResponse();

            // repeated string için Add ile ekleme yapýlýr
            response.Brands.Add("BMW");
            response.Brands.Add("Mercedes");
            response.Brands.Add("Audi");
            response.Brands.Add("Volkswagen");

            return Task.FromResult(response);
        }
    }
}


