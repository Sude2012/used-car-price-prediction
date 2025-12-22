

using CarPrice.Business.Interfaces;
using CarPrice.Core.DTOs;
using CarPrice.Core.Entities;
using CarPrice.DataAccess.Repositories;
using System;

namespace CarPrice.Business.Concrete
{
    public class AuthService : IAuthService
    {
        private readonly IUserRepository _repo;

        public AuthService(IUserRepository repo)
        {
            _repo = repo;
        }

        public bool Register(RegisterDTO dto)
        {
            try
            {
                // Bu email daha önce kayıtlı mı?
                var existingUser = _repo.GetByEmail(dto.Email);

                if (existingUser != null)
                {
                    Console.WriteLine("REGISTER ERROR: Email already exists.");
                    return false;
                }

                // Repository'ye kayıt yaptır
                return _repo.Register(dto);
            }
            catch (Exception ex)
            {
                Console.WriteLine("AUTH REGISTER ERROR → " + ex.Message);
                return false;
            }
        }

        public User Login(LoginDTO dto)
        {
            try
            {
                // Repository login'i yapıyor (şifreyi de kontrol ediyor)
                var user = _repo.Login(dto);
                return user;
            }
            catch (Exception ex)
            {
                Console.WriteLine("AUTH LOGIN ERROR → " + ex.Message);
                return null;
            }
        }
    }
}
