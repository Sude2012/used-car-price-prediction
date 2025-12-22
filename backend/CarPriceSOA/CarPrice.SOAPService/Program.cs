using CarPrice.Business.Interfaces;
using CarPrice.Business.Concrete;
using CarPrice.SOAPService.Services;
using SoapCore;

var builder = WebApplication.CreateBuilder(args);

// ?? EN KRÝTÝK SATIR (EKSÝKTÝ)
builder.Services.AddSoapCore();

// DI
builder.Services.AddScoped<ICarService, CarManager>();
builder.Services.AddScoped<IVehicleSoapService, VehicleSoapService>();

builder.Services.AddControllers();

var app = builder.Build();

app.UseRouting();

app.UseEndpoints(endpoints =>
{
    // SOAP endpoint
    endpoints.UseSoapEndpoint<IVehicleSoapService>(
        "/soap/vehicle",
        new SoapEncoderOptions(),
        SoapSerializer.DataContractSerializer
    );

    // Normal API controller'lar
    endpoints.MapControllers();
});

app.Run();







/*EN SON BUYDUUUUUU
using CarPrice.Business.Concrete;
using CarPrice.Business.Interfaces;
using CarPrice.SOAPService.Services;
using SoapCore;

var builder = WebApplication.CreateBuilder(args);

// DI
builder.Services.AddScoped<ICarService, CarManager>();
builder.Services.AddScoped<IVehicleSoapService, VehicleSoapService>();

builder.Services.AddControllers();

var app = builder.Build();

app.UseRouting();

// TEK bir UseEndpoints olacak
app.UseEndpoints(endpoints =>
{
    // SOAP endpoint
    endpoints.UseSoapEndpoint<IVehicleSoapService>("/soap/vehicle",
        new SoapEncoderOptions(),
        SoapSerializer.DataContractSerializer);

    // Normal API controller endpointleri
    endpoints.MapControllers();
});

app.Run();

*/

/*

using CarPrice.Business.Concrete;
using CarPrice.Business.Interfaces;
using CarPrice.DataAccess.Repositories;
using CarPrice.SOAPService.Services;
using SoapCore;

var builder = WebApplication.CreateBuilder(args);

// ----------------------------------------------------------
// DEPENDENCY INJECTION
// ----------------------------------------------------------
builder.Services.AddScoped<ICarService, CarManager>();

// Auth iþlemleri için gereken DI
builder.Services.AddScoped<IUserRepository, UserRepository>();
builder.Services.AddScoped<IAuthService, AuthService>();

// SOAP Service
builder.Services.AddScoped<IVehicleSoapService, VehicleSoapService>();

// Controllers
builder.Services.AddControllers();

// Swagger
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

// ----------------------------------------------------------
// MIDDLEWARE
// ----------------------------------------------------------
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseRouting();

// SOAP Endpoint
app.UseSoapEndpoint<IVehicleSoapService>("/soap/vehicle",
    new SoapEncoderOptions(),
    SoapSerializer.DataContractSerializer);

// REST API endpointleri (AuthController + CarController)
app.MapControllers();

app.Run();
*/