using Microsoft.AspNetCore.Mvc;
using CarPrice.Business.Concrete;
using CarPrice.Core.DTOs;
using CarPrice.DataAccess.Repositories;

namespace CarPrice.ApiGateway.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class AuthController : ControllerBase
    {
        private readonly AuthService _authService;

        public AuthController()
        {
            _authService = new AuthService(new UserRepository());
        }

        [HttpPost("register")]
        public IActionResult Register([FromBody] RegisterDTO dto)
        {
            bool result = _authService.Register(dto);

            if (result)
                return Ok(new { message = "Kayıt başarılı." });

            return BadRequest(new { message = "Kayıt başarısız." });
        }






        [HttpPost("login")]
        public IActionResult Login([FromBody] LoginDTO dto)
        {
            var user = _authService.Login(dto);

            if (user == null)
                return Unauthorized(new { message = "E-posta veya şifre hatalı!" });

            // ✅ Frontend uyumlu (küçük harfli) JSON
            return Ok(new
            {
                message = "Giriş başarılı!",
                user = new
                {
                    userId = user.UserId,
                    firstName = user.FirstName,
                    lastName = user.LastName,
                    email = user.Email,
                    role = user.Role
                }
            });
        }
    }
}