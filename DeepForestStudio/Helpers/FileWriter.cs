using DeepForestStudio.Data;
using Newtonsoft.Json;
using System.IO;

namespace DeepForestStudio.Helpers
{
    public static class FileWriter
    {
        public static void Write(string path, DeepForestConfig data)
        {
            var json = JsonConvert.SerializeObject(data, new JsonSerializerSettings
            {
                Formatting = Formatting.Indented,
                TypeNameHandling = TypeNameHandling.None,
                NullValueHandling = NullValueHandling.Ignore
            });

            File.WriteAllText(path, json);
        }
    }
}
