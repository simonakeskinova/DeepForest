namespace DeepForestStudio.Forms
{
    partial class ClassifierSelectForm
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.SelectButton = new System.Windows.Forms.Button();
            this.CancelButton = new System.Windows.Forms.Button();
            this.groupBox1 = new System.Windows.Forms.GroupBox();
            this.label3 = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.KFoldsNumericUpDown = new System.Windows.Forms.NumericUpDown();
            this.EstimatorsCountNumericUpDown = new System.Windows.Forms.NumericUpDown();
            this.label1 = new System.Windows.Forms.Label();
            this.TypeComboBox = new System.Windows.Forms.ComboBox();
            this.groupBox1.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.KFoldsNumericUpDown)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.EstimatorsCountNumericUpDown)).BeginInit();
            this.SuspendLayout();
            // 
            // SelectButton
            // 
            this.SelectButton.Location = new System.Drawing.Point(218, 106);
            this.SelectButton.Name = "SelectButton";
            this.SelectButton.Size = new System.Drawing.Size(75, 23);
            this.SelectButton.TabIndex = 6;
            this.SelectButton.Text = "Запази";
            this.SelectButton.UseVisualStyleBackColor = true;
            this.SelectButton.Click += new System.EventHandler(this.SelectButton_Click);
            // 
            // CancelButton
            // 
            this.CancelButton.Location = new System.Drawing.Point(299, 106);
            this.CancelButton.Name = "CancelButton";
            this.CancelButton.Size = new System.Drawing.Size(75, 23);
            this.CancelButton.TabIndex = 7;
            this.CancelButton.Text = "Откажи";
            this.CancelButton.UseVisualStyleBackColor = true;
            this.CancelButton.Click += new System.EventHandler(this.CancelButton_Click);
            // 
            // groupBox1
            // 
            this.groupBox1.Controls.Add(this.label3);
            this.groupBox1.Controls.Add(this.label2);
            this.groupBox1.Controls.Add(this.KFoldsNumericUpDown);
            this.groupBox1.Controls.Add(this.EstimatorsCountNumericUpDown);
            this.groupBox1.Controls.Add(this.label1);
            this.groupBox1.Controls.Add(this.TypeComboBox);
            this.groupBox1.Dock = System.Windows.Forms.DockStyle.Top;
            this.groupBox1.Location = new System.Drawing.Point(0, 0);
            this.groupBox1.Name = "groupBox1";
            this.groupBox1.Size = new System.Drawing.Size(386, 100);
            this.groupBox1.TabIndex = 8;
            this.groupBox1.TabStop = false;
            this.groupBox1.Text = "Параметри";
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(12, 74);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(112, 13);
            this.label3.TabIndex = 11;
            this.label3.Text = "Брой дървета в гора";
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(12, 48);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(103, 13);
            this.label2.TabIndex = 10;
            this.label2.Text = "к (крос валидация)";
            // 
            // KFoldsNumericUpDown
            // 
            this.KFoldsNumericUpDown.Location = new System.Drawing.Point(130, 46);
            this.KFoldsNumericUpDown.Maximum = new decimal(new int[] {
            500,
            0,
            0,
            0});
            this.KFoldsNumericUpDown.Name = "KFoldsNumericUpDown";
            this.KFoldsNumericUpDown.Size = new System.Drawing.Size(89, 20);
            this.KFoldsNumericUpDown.TabIndex = 9;
            this.KFoldsNumericUpDown.Value = new decimal(new int[] {
            3,
            0,
            0,
            0});
            this.KFoldsNumericUpDown.ValueChanged += new System.EventHandler(this.KFoldsNumericUpDown_ValueChanged);
            // 
            // EstimatorsCountNumericUpDown
            // 
            this.EstimatorsCountNumericUpDown.Location = new System.Drawing.Point(130, 72);
            this.EstimatorsCountNumericUpDown.Maximum = new decimal(new int[] {
            500,
            0,
            0,
            0});
            this.EstimatorsCountNumericUpDown.Name = "EstimatorsCountNumericUpDown";
            this.EstimatorsCountNumericUpDown.Size = new System.Drawing.Size(89, 20);
            this.EstimatorsCountNumericUpDown.TabIndex = 8;
            this.EstimatorsCountNumericUpDown.Value = new decimal(new int[] {
            50,
            0,
            0,
            0});
            this.EstimatorsCountNumericUpDown.ValueChanged += new System.EventHandler(this.EstimatorsCountNumericUpDown_ValueChanged);
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(12, 22);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(102, 13);
            this.label1.TabIndex = 7;
            this.label1.Text = "Тип класификатор";
            // 
            // TypeComboBox
            // 
            this.TypeComboBox.FormattingEnabled = true;
            this.TypeComboBox.Location = new System.Drawing.Point(130, 19);
            this.TypeComboBox.Name = "TypeComboBox";
            this.TypeComboBox.Size = new System.Drawing.Size(244, 21);
            this.TypeComboBox.TabIndex = 6;
            this.TypeComboBox.SelectedIndexChanged += new System.EventHandler(this.TypeComboBox_SelectedIndexChanged);
            // 
            // ClassifierSelectForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(386, 136);
            this.Controls.Add(this.groupBox1);
            this.Controls.Add(this.CancelButton);
            this.Controls.Add(this.SelectButton);
            this.Name = "ClassifierSelectForm";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.groupBox1.ResumeLayout(false);
            this.groupBox1.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.KFoldsNumericUpDown)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.EstimatorsCountNumericUpDown)).EndInit();
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.Button SelectButton;
        private System.Windows.Forms.Button CancelButton;
        private System.Windows.Forms.GroupBox groupBox1;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.NumericUpDown KFoldsNumericUpDown;
        private System.Windows.Forms.NumericUpDown EstimatorsCountNumericUpDown;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.ComboBox TypeComboBox;
    }
}