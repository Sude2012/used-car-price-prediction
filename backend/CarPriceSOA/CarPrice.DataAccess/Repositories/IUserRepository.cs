

using CarPrice.Core.DTOs;
using CarPrice.Core.Entities;

namespace CarPrice.DataAccess.Repositories
{
    public interface IUserRepository
    {
        bool Register(RegisterDTO dto);
        User Login(LoginDTO dto);
        User GetByEmail(string email);
    }
}
