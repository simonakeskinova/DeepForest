using System.Collections.Generic;

namespace DeepForestStudio.Data
{
    public class CascadeConfig
    {
        public string Name { get; set; }
        public int MaxLevelCount { get; set; }
        public bool KeepModelInMemory { get; set; }
        public string TempDirectory { get; set; }
        public List<Classifier> Classifiers { get; set; }

        public CascadeConfig()
        {
            Classifiers = new List<Classifier>();
        }
    }
}
