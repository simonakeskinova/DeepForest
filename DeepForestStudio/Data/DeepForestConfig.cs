using Newtonsoft.Json;
using Newtonsoft.Json.Converters;
using System.Collections.Generic;

namespace DeepForestStudio.Data
{
    public class DeepForestConfig
    {
        public int ClassesCount { get; set; }
        public bool ZeroBasedClasses { get; set; }

        [JsonConverter(typeof(StringEnumConverter))]
        public CascadeType? CascadeType { get; set; }
        public DataConfig Data { get; set; }
        public ScanningConfig Scanning { get; set; }
        public CascadeConfig Cascade { get; set; }

        public DeepForestConfig()
        {
            Data = new DataConfig
            {
#if DEBUG
                TrainDataPath = @"E:\Source\DeepForestStudio\data\train.txt",
                TestDataPath = @"E:\Source\DeepForestStudio\data\test.txt"
#endif
            };
            Scanning = new ScanningConfig
            {
#if DEBUG
                Name = "scanning_test",
                TempDirectory = @"E:\Source\DeepForestStudio\data\temp\",
                KeepModelInMemory = false,
                ContextPOSSize = 10,
                ContextSize = 5,
                WordSize = 300,
                Scanners = new List<Scanner>
                {
                    new Scanner
                    {
                        WindowSize = 3,
                        Classifiers = new List<Classifier>
                        {
                            new Classifier
                            {
                                ClassifierType = ClassifierType.RandomForest,
                                EstimatorsCount = 50,
                                KFolds = 3
                            },
                            new Classifier
                            {
                                ClassifierType = ClassifierType.ExtraTrees,
                                EstimatorsCount = 50,
                                KFolds = 3
                            }
                        }
                    },
                    new Scanner
                    {
                        WindowSize = 5,
                        Classifiers = new List<Classifier>
                        {
                            new Classifier
                            {
                                ClassifierType = ClassifierType.RandomForest,
                                EstimatorsCount = 50,
                                KFolds = 3
                            },
                            new Classifier
                            {
                                ClassifierType = ClassifierType.ExtraTrees,
                                EstimatorsCount = 50,
                                KFolds = 3
                            }
                        }
                    },
                    new Scanner
                    {
                        WindowSize = 7,
                        Classifiers = new List<Classifier>
                        {
                            new Classifier
                            {
                                ClassifierType = ClassifierType.RandomForest,
                                EstimatorsCount = 50,
                                KFolds = 3
                            },
                            new Classifier
                            {
                                ClassifierType = ClassifierType.ExtraTrees,
                                EstimatorsCount = 50,
                                KFolds = 3
                            }
                        }
                    }
                }
#endif      
            };
            Cascade = new CascadeConfig
            {
                KeepModelInMemory = false,
#if DEBUG
                MaxLevelCount = 5,
                Name = "cascade_test",

                TempDirectory = @"E:\Source\DeepForestStudio\data\temp\",

                Classifiers = new List<Classifier>
                {
                    new Classifier
                    {
                        ClassifierType = ClassifierType.RandomForest,
                        EstimatorsCount = 500,
                        KFolds = 3
                    },
                    new Classifier
                    {
                        ClassifierType = ClassifierType.RandomForest,
                        EstimatorsCount = 500,
                        KFolds = 3
                    },
                    new Classifier
                    {
                        ClassifierType = ClassifierType.ExtraTrees,
                        EstimatorsCount = 500,
                        KFolds = 3
                    },
                    new Classifier
                    {
                        ClassifierType = ClassifierType.ExtraTrees,
                        EstimatorsCount = 500,
                        KFolds = 3
                    }
                }
#endif
            };
        }
    }
}
