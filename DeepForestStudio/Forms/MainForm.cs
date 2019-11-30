using DeepForestStudio.Data;
using DeepForestStudio.Forms;
using DeepForestStudio.Helpers;
using System;
using System.Windows.Forms;
using Microsoft.WindowsAPICodePack.Dialogs;
using System.Diagnostics;
using System.Collections.Generic;
using System.IO;
using System.Configuration;
using System.Threading.Tasks;

namespace DeepForestStudio
{
    public partial class DeepForestForm : Form
    {
        private string _deepForestConfigPath = "";
        private string _pythonFile = "pythoncode/python_test.py";

        private DeepForestConfig _deepForestConfig = new DeepForestConfig
        {
#if DEBUG
            ClassesCount = 10,
            ZeroBasedClasses = false
#endif
        };

        private int _selectedClassifierIndex = -1;
        private int _selectedScannerIndex = -1;
        private int _selectedWindowIndex = 0;
        bool _refreshingUI = false;

        public DeepForestForm()
        {
            InitializeComponent();

            CascadeTypeComboBox.Items.AddRange(new object[]
            {
                CascadeType.MixedCascade,
                CascadeType.SequentialCascade
            });

            RefreshUI(true, true);
        }

        private void RefreshUI(bool invalidateList = false, bool invalidateTabControl = false)
        {
            _refreshingUI = true;

            try
            {
                TrainDataTextBox.Text =
                    _deepForestConfig.Data.TrainDataPath;
                TestDataTextBox.Text =
                    _deepForestConfig.Data.TestDataPath;
                ClassesCountNumericUpDown.Value =
                    _deepForestConfig.ClassesCount;
                ZeroBasedClassesCheckBox.Checked =
                    _deepForestConfig.ZeroBasedClasses;
                CascadeTypeComboBox.SelectedIndex =
                        _deepForestConfig.CascadeType != null
                        ? CascadeTypeComboBox.Items.IndexOf(_deepForestConfig.CascadeType)
                        : -1;

                AddScanningProcedureCheckBox.Checked =
                    _deepForestConfig.Scanning == null
                    ? false
                    : true;
                Scanning_GroupBox.Visible =
                    AddScanningProcedureCheckBox.Checked;

                if (_deepForestConfig.Scanning != null)
                {
                    Scanning_TempDirectoryTextBox.Text =
                        _deepForestConfig.Scanning.TempDirectory;
                    Scanning_TestNameTextBox.Text =
                        _deepForestConfig.Scanning.Name;
                    Scanning_ContextSizeNumericUpDown.Value =
                        _deepForestConfig.Scanning.ContextSize;
                    Scanning_POSSizeNumericUpDown.Value =
                        _deepForestConfig.Scanning.ContextPOSSize;
                    Scanning_ContextWordSizeNumericUpDown.Value =
                        _deepForestConfig.Scanning.WordSize;
                    Scanning_KeepModelInMemoryCheckBox.Checked =
                        _deepForestConfig.Scanning.KeepModelInMemory;
                }

                Cascade_TempDirectoryTextBox.Text =
                    _deepForestConfig.Cascade.TempDirectory;
                Cascade_TestNameTextBox.Text =
                    _deepForestConfig.Cascade.Name;
                Cascade_KeepModelInMemoryCheckBox.Checked =
                    _deepForestConfig.Cascade.KeepModelInMemory;
                Cascade_MaxLevelsCountNumericUpDown.Value =
                    _deepForestConfig.Cascade.MaxLevelCount;

                if (invalidateTabControl)
                {
                    ReloadTabControlPages();
                }

                if (invalidateList)
                {                    
                    ReloadScanningListViewItems();
                    ReloadCascadeListViewItems();
                }
                
                Scanning_ScannersListView.SelectedIndices.Clear();
                Cascade_ClassifiersListView.SelectedIndices.Clear();

                if (_selectedScannerIndex > -1)
                    Scanning_ScannersListView.SelectedIndices.Add(_selectedScannerIndex);
                if (_selectedClassifierIndex > -1)
                    Cascade_ClassifiersListView.SelectedIndices.Add(_selectedClassifierIndex);

                ConfigFilePathTextBox.Text = _deepForestConfigPath;

                Scanning_RemoveWindowButton.Enabled = Scanning_WindowsTabControl.TabPages.Count > 1;
                Scanning_RemoveScannerButton.Enabled = _selectedScannerIndex > -1;
                Cascade_RemoveClassifierButton.Enabled = _selectedClassifierIndex > -1;
                SaveConfigButton.Enabled = _deepForestConfig.Cascade.Classifiers.Count > 0;
            }
            finally
            {
                _refreshingUI = false;
            }
        }

        private void RefreshWindowUI()
        {
            ReloadScanningListViewItems();

            Scanning_WindowSizeNumericUpDown.Value =
                _deepForestConfig.Scanning.Scanners[_selectedWindowIndex].WindowSize;
        }

        private void ReloadTabControlPages()
        {
            Scanning_WindowsTabControl.TabPages.Clear();
            foreach (var scanner in _deepForestConfig.Scanning.Scanners)
            {
                var title = string.Format("Прозорец {0}", (Scanning_WindowsTabControl.TabCount + 1).ToString());
                var tabPage = new TabPage(title);
                tabPage.UseVisualStyleBackColor = true;

                Scanning_WindowsTabControl.TabPages.Add(tabPage);
            }

            _selectedWindowIndex = 0;
            Scanning_WindowsTabControl.SelectedTab.Controls.Add(WindowPanel);
            RefreshWindowUI();
        }
               
        private void ReloadCascadeListViewItems()
        {
            Cascade_ClassifiersListView.Items.Clear();
            foreach (var classifier in _deepForestConfig.Cascade.Classifiers)
            {
                var listItem = new ListViewItem(classifier.ClassifierType.ToString());

                listItem.SubItems.Add(classifier.KFolds.ToString());
                listItem.SubItems.Add(classifier.EstimatorsCount.ToString());

                Cascade_ClassifiersListView.Items.Add(listItem);
            }
        }

        private void ReloadScanningListViewItems()
        {
            Scanning_ScannersListView.Items.Clear();
            foreach (var classifier in _deepForestConfig.Scanning.Scanners[_selectedWindowIndex].Classifiers)
            {
                var listItem = new ListViewItem(classifier.ClassifierType.ToString());

                listItem.SubItems.Add(classifier.KFolds.ToString());
                listItem.SubItems.Add(classifier.EstimatorsCount.ToString());

                Scanning_ScannersListView.Items.Add(listItem);
            }
        }

        private void SaveDeepForestConfig()
        {
            using (var dialog = DialogHelper.SaveFile("DeepForest config files (*.json)|*.json", ".json"))
            {
                var result = dialog.ShowDialog(this);

                if (result == DialogResult.OK)
                {
                    _deepForestConfigPath = dialog.FileName;
                    FileWriter.Write(_deepForestConfigPath, _deepForestConfig);

                    RefreshUI();

                    MessageBox.Show("Конфигурационният файл за DeepForest е записан успешно.", "Успешно");
                }
            }
        }

        private void TrainDataButton_Click(object sender, EventArgs e)
        {
            using (var dialog = DialogHelper.OpenFile())
            {
                var result = dialog.ShowDialog(this);

                if (result == DialogResult.OK)
                {
                    _deepForestConfig.Data.TrainDataPath = dialog.FileName;

                    RefreshUI();
                }
            }
        }

        private void TestDataButton_Click(object sender, EventArgs e)
        {
            using (var dialog = DialogHelper.OpenFile())
            {
                var result = dialog.ShowDialog(this);

                if (result == DialogResult.OK)
                {
                    _deepForestConfig.Data.TestDataPath = dialog.FileName;

                    RefreshUI();
                }
            }
        }

        private void ClassesCountNumericUpDown_ValueChanged(object sender, EventArgs e)
        {
            if (_refreshingUI)
                return;

            _deepForestConfig.ClassesCount = (int)ClassesCountNumericUpDown.Value;
        }

        private void Scanning_TestNameTextBox_TextChanged(object sender, EventArgs e)
        {
            if (_refreshingUI)
                return;

            _deepForestConfig.Scanning.Name = Scanning_TestNameTextBox.Text;
        }

        private void Scanning_TempDirectoryButton_Click(object sender, EventArgs e)
        {
            using (var dialog = DialogHelper.SelectFolder())
            {
                var result = dialog.ShowDialog();

                if (result == CommonFileDialogResult.Ok)
                {
                    _deepForestConfig.Scanning.TempDirectory = dialog.FileName;

                    RefreshUI();
                }
            }
        }

        private void Scanning_ContextSizeNumericUpDown_ValueChanged(object sender, EventArgs e)
        {
            if (_refreshingUI)
                return;

            _deepForestConfig.Scanning.ContextSize = (int)Scanning_ContextSizeNumericUpDown.Value;
        }

        private void Scanning_POSSizeNumericUpDown_ValueChanged(object sender, EventArgs e)
        {
            if (_refreshingUI)
                return;

            _deepForestConfig.Scanning.ContextPOSSize = (int)Scanning_POSSizeNumericUpDown.Value;
        }

        private void Scanning_ContextWordSizeNumericUpDown_ValueChanged(object sender, EventArgs e)
        {
            if (_refreshingUI)
                return;

            _deepForestConfig.Scanning.WordSize = (int)Scanning_ContextWordSizeNumericUpDown.Value;
        }

        private void Scanning_KeepModelInMemoryCheckBox_CheckedChanged(object sender, EventArgs e)
        {
            if (_refreshingUI)
                return;

            _deepForestConfig.Scanning.KeepModelInMemory = Scanning_KeepModelInMemoryCheckBox.Checked;
        }

        private void Scanning_AddScannerButton_Click(object sender, EventArgs e)
        {
            using (var dialog = new ClassifierSelectForm(null))
            {
                var result = dialog.ShowDialog(this);

                if (result == DialogResult.OK)
                {
                    _deepForestConfig.Scanning.Scanners[_selectedWindowIndex].Classifiers.Add(dialog.Classifier);

                    RefreshUI(true);

                    Scanning_ScannersListView.Focus();
                }
            }
        }

        private void Scanning_RemoveScannerButton_Click(object sender, EventArgs e)
        {
            if (_selectedScannerIndex < 0 ||
                _selectedScannerIndex >= _deepForestConfig.Scanning.Scanners.Count)
                return;

            _deepForestConfig.Scanning.Scanners.RemoveAt(_selectedScannerIndex);
            _selectedScannerIndex =
                Math.Min(_selectedScannerIndex, _deepForestConfig.Scanning.Scanners.Count - 1);

            RefreshUI(true);

            Scanning_ScannersListView.Focus();
        }

        private void Scanning_ScannersListView_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (_refreshingUI)
                return;

            _selectedScannerIndex = Scanning_ScannersListView.SelectedIndices.Count > 0
                ? Scanning_ScannersListView.SelectedIndices[0]
                : -1;

            if (_selectedScannerIndex >= _deepForestConfig.Scanning.Scanners.Count)
                _selectedScannerIndex = -1;

            RefreshUI();
        }

        private void Scanning_ScannersListView_DoubleClick(object sender, EventArgs e)
        {
            if (_selectedScannerIndex < 0 ||
                _selectedScannerIndex >= _deepForestConfig.Scanning.Scanners.Count)
                return;

            using (var dialog = new ClassifierSelectForm(_deepForestConfig.Scanning.Scanners[_selectedWindowIndex].Classifiers[_selectedScannerIndex]))
            {
                var result = dialog.ShowDialog(this);

                if (result == DialogResult.OK)
                {
                    _deepForestConfig.Scanning.Scanners[_selectedWindowIndex].Classifiers[_selectedScannerIndex] = dialog.Classifier;

                    RefreshUI(true);

                    Scanning_ScannersListView.Focus();
                }
            }
        }

        private void Cascade_TempDirectoryButton_Click(object sender, EventArgs e)
        {
            using (var dialog = DialogHelper.SelectFolder())
            {
                var result = dialog.ShowDialog();

                if (result == CommonFileDialogResult.Ok)
                {
                    _deepForestConfig.Cascade.TempDirectory = dialog.FileName;

                    RefreshUI();
                }
            }
        }

        private void Cascade_TestNameTextBox_TextChanged(object sender, EventArgs e)
        {
            if (_refreshingUI)
                return;

            _deepForestConfig.Cascade.Name = Cascade_TestNameTextBox.Text;
        }

        private void Cascade_KeepModelInMemoryCheckBox_CheckedChanged(object sender, EventArgs e)
        {
            if (_refreshingUI)
                return;

            _deepForestConfig.Cascade.KeepModelInMemory = Cascade_KeepModelInMemoryCheckBox.Checked;
        }

        private void Cascade_MaxLevelsCountNumericUpDown_ValueChanged(object sender, EventArgs e)
        {
            if (_refreshingUI)
                return;

            _deepForestConfig.Cascade.MaxLevelCount = (int)Cascade_MaxLevelsCountNumericUpDown.Value;
        }

        private void Cascade_AddClassifierButton_Click(object sender, EventArgs e)
        {
            using (var dialog = new ClassifierSelectForm(null))
            {
                var result = dialog.ShowDialog(this);

                if (result == DialogResult.OK)
                {
                    _deepForestConfig.Cascade.Classifiers.Add(dialog.Classifier);

                    RefreshUI(true);

                    Cascade_ClassifiersListView.Focus();
                }
            }
        }

        private void Cascade_RemoveClassifierButton_Click(object sender, EventArgs e)
        {
            if (_selectedClassifierIndex < 0 ||
                _selectedClassifierIndex >= _deepForestConfig.Cascade.Classifiers.Count)
                return;

            _deepForestConfig.Cascade.Classifiers.RemoveAt(_selectedClassifierIndex);
            _selectedClassifierIndex =
                Math.Min(_selectedClassifierIndex, _deepForestConfig.Cascade.Classifiers.Count - 1);

            RefreshUI(true);

            Cascade_ClassifiersListView.Focus();
        }

        private void Cascade_ClassifiersListView_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (_refreshingUI)
                return;

            _selectedClassifierIndex = Cascade_ClassifiersListView.SelectedIndices.Count > 0
                ? Cascade_ClassifiersListView.SelectedIndices[0]
                : -1;

            if (_selectedClassifierIndex >= _deepForestConfig.Cascade.Classifiers.Count)
                _selectedClassifierIndex = -1;

            RefreshUI();
        }

        private void Cascade_ClassifiersListView_DoubleClick(object sender, EventArgs e)
        {
            if (_selectedClassifierIndex < 0 ||
                _selectedClassifierIndex >= _deepForestConfig.Cascade.Classifiers.Count)
                return;

            using (var dialog = new ClassifierSelectForm(_deepForestConfig.Cascade.Classifiers[_selectedClassifierIndex]))
            {
                var result = dialog.ShowDialog(this);

                if (result == DialogResult.OK)
                {
                    _deepForestConfig.Cascade.Classifiers[_selectedClassifierIndex] = dialog.Classifier;

                    RefreshUI(true);

                    Cascade_ClassifiersListView.Focus();
                }
            }
        }

        private void Scanning_AddWindowButton_Click(object sender, EventArgs e)
        {
            var tabPage = new TabPage(string.Format("Прозорец {0}", (Scanning_WindowsTabControl.TabCount + 1).ToString()));
            tabPage.UseVisualStyleBackColor = true;

            _deepForestConfig.Scanning.Scanners.Add(new Scanner());

            Scanning_WindowsTabControl.TabPages.Add(tabPage);
            Scanning_WindowsTabControl.SelectedTab = tabPage;

            RefreshUI(true, true);
        }

        private void Scanning_WindowsTabControl_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (Scanning_WindowsTabControl.SelectedTab != null)
            {
                _selectedWindowIndex = Scanning_WindowsTabControl.SelectedIndex;

                Scanning_WindowsTabControl.SelectedTab.Controls.Add(WindowPanel);

                RefreshWindowUI();
            }
        }

        private void Scanning_RemoveWindowButton_Click(object sender, EventArgs e)
        {
            if (_selectedWindowIndex < 0 ||
                _selectedWindowIndex >= _deepForestConfig.Scanning.Scanners.Count)
                return;

            _deepForestConfig.Scanning.Scanners.RemoveAt(_selectedWindowIndex);
            _selectedWindowIndex =
                Math.Min(_selectedWindowIndex, _deepForestConfig.Scanning.Scanners.Count - 1);

            //ReloadTabControlPages();
            RefreshUI(true, true); 
        }

        private void Scanning_WindowSizeNumericUpDown_ValueChanged(object sender, EventArgs e)
        {
            if (_refreshingUI)
                return;

            _deepForestConfig.Scanning.Scanners[_selectedWindowIndex].WindowSize = (int)Scanning_WindowSizeNumericUpDown.Value;
        }

        private void SaveConfigButton_Click(object sender, EventArgs e)
        {
            SaveDeepForestConfig();
        }

        private void ProcessOutputHandler(string data)
        {
            if (InvokeRequired)
            {
                Invoke((MethodInvoker)delegate () { ProcessOutputHandler(data); });
                return;
            }

            if (data != null)
            {
                ResultTextBox.AppendText(data);
                ResultTextBox.AppendText(Environment.NewLine);
            }
        }

        public void run_cmd()
        {
            ProcessStartInfo start = new ProcessStartInfo();

            var argument = Path.Combine(Path.GetDirectoryName(Application.ExecutablePath), _pythonFile);
            argument = argument.Replace("\\", "/");

            var parameter = ConfigFilePathTextBox.Text;
            parameter = parameter.Replace("\\", "/");

            start.FileName = ConfigurationManager.AppSettings["PythonPath"]; 

            start.Arguments = string.Format("-u \"{0}\" --model {1}", argument, parameter);
            start.UseShellExecute = false;
            start.CreateNoWindow = true; 
            start.RedirectStandardOutput = true;
            start.RedirectStandardError = true;

            Task.Factory.StartNew(() =>
            {
                Invoke((MethodInvoker)delegate ()
                {
                    Enabled = false;
                });

                try
                {
                    using (Process process = new Process
                    {
                        StartInfo = start
                    })
                    {
                        process.OutputDataReceived += (sender, args) => ProcessOutputHandler(args.Data);
                        process.ErrorDataReceived += (sender, args) => {
                            if (!string.IsNullOrWhiteSpace(args.Data))
                                ProcessOutputHandler("ERROR:    " + args.Data);
                            };
                        
                        process.Start();
                        process.BeginOutputReadLine();
                        process.BeginErrorReadLine();

                        process.WaitForExit();
                    }
                }
                finally
                {
                    Invoke((MethodInvoker)delegate ()
                    {
                        Enabled = true;
                    });
                }
            }, TaskCreationOptions.LongRunning);
        }

        private void StartTest()
        {
            run_cmd();
        }

        private void StartTestButton_Click(object sender, EventArgs e)
        {
            ResultTextBox.AppendText(
                string.Format("Начало на тест с DeepForest в {0}", DateTime.Now.ToString()));
            ResultTextBox.AppendText(Environment.NewLine);

            StartTest();
        }

        private void ZeroBasedClassesCheckBox_CheckedChanged(object sender, EventArgs e)
        {
            if (_refreshingUI)
                return;

            _deepForestConfig.ZeroBasedClasses = ZeroBasedClassesCheckBox.Checked;
        }

        private void CascadeTypeComboBox_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (_refreshingUI)
                return;

            _deepForestConfig.CascadeType =
                (CascadeType)CascadeTypeComboBox.SelectedItem;

            RefreshUI();
        }

        private void AddScanningProcedureCheckBox_CheckedChanged(object sender, EventArgs e)
        {
            if (_refreshingUI)
                return;

            _deepForestConfig.Scanning =
                AddScanningProcedureCheckBox.Checked
                ? new ScanningConfig
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
                }
                : null;

            RefreshUI();
        }

        private void ConfigFilePathButton_Click(object sender, EventArgs e)
        {
            using (var dialog = DialogHelper.OpenFile())
            {
                var result = dialog.ShowDialog(this);

                if (result == DialogResult.OK)
                {
                    ConfigFilePathTextBox.Text = dialog.FileName;
                }
            }
        }
    }
}
