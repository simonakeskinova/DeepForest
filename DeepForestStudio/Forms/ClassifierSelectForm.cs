using DeepForestStudio.Data;
using System;
using System.Windows.Forms;

namespace DeepForestStudio.Forms
{
    public partial class ClassifierSelectForm : Form
    {
        private bool _refreshingUI;

        public Classifier Classifier { get; }

        public ClassifierSelectForm(Classifier classifier)
        {
            InitializeComponent();

            SetStyle(ControlStyles.AllPaintingInWmPaint |
                     ControlStyles.UserPaint |
                     ControlStyles.OptimizedDoubleBuffer, true);

            TypeComboBox.Items.AddRange(new object[]
            {
                ClassifierType.RandomForest,
                ClassifierType.ExtraTrees
            });
            
            if (classifier == null)
            {
                Classifier = new Classifier
                {
                    KFolds = 3,
                    EstimatorsCount = 50
                };
                Text = "Добавяне на класификатор";
            }
            else
            {
                Classifier = new Classifier
                {
                    ClassifierType = classifier.ClassifierType,
                    KFolds = classifier.KFolds,
                    EstimatorsCount = classifier.EstimatorsCount
                };
                Text = "Редакция на класификатор";
            }

            RefreshUI();
        }

        private void RefreshUI()
        {
            _refreshingUI = true;

            try
            {
                TypeComboBox.SelectedIndex = Classifier.ClassifierType != null
                    ? TypeComboBox.Items.IndexOf(Classifier.ClassifierType)
                    : -1;

                KFoldsNumericUpDown.Value = Classifier.KFolds;
                EstimatorsCountNumericUpDown.Value = Classifier.EstimatorsCount;
            }
            finally
            {
                _refreshingUI = false;
            }
        }

        private void SelectButton_Click(object sender, EventArgs e)
        {
            if (Classifier.ClassifierType == null)
            {
                MessageBox.Show("Полето \"Тип класификатор\" е задължително!", "Грешка");

                return;
            }

            DialogResult = DialogResult.OK;
        }

        private void CancelButton_Click(object sender, EventArgs e)
        {
            DialogResult = DialogResult.Cancel;
        }

        private void TypeComboBox_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (_refreshingUI)
                return;

            Classifier.ClassifierType =
                (ClassifierType)TypeComboBox.SelectedItem;

            RefreshUI();
        }

        private void KFoldsNumericUpDown_ValueChanged(object sender, EventArgs e)
        {
            if (_refreshingUI)
                return;

            Classifier.KFolds = (int)KFoldsNumericUpDown.Value;
        }

        private void EstimatorsCountNumericUpDown_ValueChanged(object sender, EventArgs e)
        {
            if (_refreshingUI)
                return;

            Classifier.EstimatorsCount = (int)EstimatorsCountNumericUpDown.Value;
        }
    }
}
