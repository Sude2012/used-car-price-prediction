

using CarPrice.Business.Concrete;
using CarPrice.Business.Interfaces;
using CarPrice.DataAccess.Repositories;
//using Microsoft.OpenApi.Models;

var builder = WebApplication.CreateBuilder(args);

// CORS EKLE
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowVue",
        policy => policy.AllowAnyOrigin()
                        .AllowAnyHeader()
                        .AllowAnyMethod());
});

builder.Services.AddControllers();
builder.Services.AddScoped<IAuthService, AuthService>();
builder.Services.AddScoped<IUserRepository, UserRepository>();

builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

app.UseSwagger();
app.UseSwaggerUI();

app.UseHttpsRedirection();

// CORS burada!!!
app.UseCors("AllowVue");

app.UseAuthorization();

app.MapControllers();

app.Run();
