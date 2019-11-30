using Newtonsoft.Json;
using Newtonsoft.Json.Converters;

namespace DeepForestStudio.Data
{
    public class Classifier
    {
        [JsonConverter(typeof(StringEnumConverter))]
        public ClassifierType? ClassifierType { get; set; }
        public int KFolds { get; set; }
        public int EstimatorsCount { get; set; }
    }

    public enum ClassifierType
    {
        RandomForest,
        ExtraTrees
    }
}
