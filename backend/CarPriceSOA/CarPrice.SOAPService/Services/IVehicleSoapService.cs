/*using System.ServiceModel;

namespace CarPrice.SOAPService.Services
{
    public class IVehicleSoapService
    {
    }
}
*/

using System.ServiceModel;

namespace CarPrice.SOAPService.Services
{
    [ServiceContract]
    public interface IVehicleSoapService
    {
        [OperationContract]
        string GetBrands();
    }
}
