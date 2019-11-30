using Newtonsoft.Json;
using Newtonsoft.Json.Converters;
using System.Collections.Generic;

namespace DeepForestStudio.Data
{
    public class ScanningConfig
    {
        public string Name { get; set; }
        public bool KeepModelInMemory { get; set; }
        public string TempDirectory { get; set; }
        public int ContextSize { get; set; }
        public int WordSize { get; set; }
        public int ContextPOSSize { get; set; }
        public List<Scanner> Scanners { get; set; }

        public ScanningConfig()
        {
            Scanners = new List<Scanner>();
            Scanners.Add(new Scanner());
        }
    }
}
