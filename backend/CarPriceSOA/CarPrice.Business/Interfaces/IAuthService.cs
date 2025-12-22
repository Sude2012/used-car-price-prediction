using CarPrice.Core.DTOs;
using CarPrice.Core.Entities;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;




namespace CarPrice.Business.Interfaces
{
    public interface IAuthService
    {
        bool Register(RegisterDTO dto);
        User Login(LoginDTO dto);
    }
}

