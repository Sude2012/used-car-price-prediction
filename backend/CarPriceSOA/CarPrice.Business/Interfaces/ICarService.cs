using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

/*namespace CarPrice.Business.Interfaces
{
    internal class ICarService
    {

        List<string> GetBrands();
    }
}
*/

namespace CarPrice.Business.Interfaces
{
    // 1. internal class yerine public interface olmalı
    public interface ICarService
    {
        // 2. Metot tanımı noktalı virgül ile bitmeli
        List<string> GetBrands();
    }
}