/*using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CarPrice.Business.Concrete
{
    internal class CarManager
    {
    }
}
*/


/*

using CarPrice.Business.Interfaces;
using CarPrice.DataAccess;

namespace CarPrice.Business.Concrete
{
    public class CarManager : ICarService
    {
        public List<string> GetBrands()
        {
            // Sadece test amacıyla DataAccess'ten veri çekiyormuş gibi yapıyoruz
            return new List<string>() { "BMW", "Mercedes", "Toyota" };
        }
    }
}
*/

using CarPrice.Business.Interfaces;
using CarPrice.DataAccess;
using System.Collections.Generic; // List için gerekli olabilir

namespace CarPrice.Business.Concrete
{
    // ICarService'in altı artık kırmızı çizilmeyecek
    public class CarManager : ICarService
    {
        public List<string> GetBrands()
        {
            // Sadece test amacıyla DataAccess'ten veri çekiyormuş gibi yapıyoruz
            return new List<string>() { "BMW", "Mercedes", "Toyota" };
        }
    }
}