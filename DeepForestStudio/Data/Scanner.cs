using System.Collections.Generic;

namespace DeepForestStudio.Data
{
    public class Scanner
    {
        public int WindowSize { get; set; }
        public List<Classifier> Classifiers { get; set; }

        public Scanner()
        {
            Classifiers = new List<Classifier>();
        }
    }
}
