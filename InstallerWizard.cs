using System;
using System.IO;
using System.Drawing;
using System.Windows.Forms;
using System.Diagnostics;
using System.Threading;

namespace AtoZScrapyInstaller
{
    public class InstallerForm : Form
    {
        private Panel bannerPanel;
        private Panel mainPanel;
        private Label titleLabel;
        private Label descLabel;
        private Label statusLabel;
        private ProgressBar progressBar;
        private TextBox pathTextBox;
        private Button browseButton;
        private Button nextButton;
        private Button cancelButton;
        private CheckBox launchCheckBox;

        private int currentStep = 0;
        private string installPath;

        public InstallerForm()
        {
            this.Text = "AtoZ Scrapy Windows 11 ED - Setup Wizard";
            this.Size = new Size(620, 440);
            this.StartPosition = FormStartPosition.CenterScreen;
            this.FormBorderStyle = FormBorderStyle.FixedDialog;
            this.MaximizeBox = false;
            this.MinimizeBox = false;

            string localAppData = Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData);
            installPath = Path.Combine(localAppData, "Programs", "AtoZ-Scrapy-Windows-11-ED");

            InitializeComponents();
            ShowStep0();
        }

        private void InitializeComponents()
        {
            bannerPanel = new Panel();
            bannerPanel.Dock = DockStyle.Left;
            bannerPanel.Width = 170;
            bannerPanel.BackColor = Color.FromArgb(0, 120, 212);

            Label bannerText = new Label();
            bannerText.Text = "🚀\n\nAtoZ Scrapy\nWindows 11 ED\nSetup Wizard";
            bannerText.ForeColor = Color.White;
            bannerText.Font = new Font("Segoe UI", 12, FontStyle.Bold);
            bannerText.Dock = DockStyle.Fill;
            bannerText.TextAlign = ContentAlignment.MiddleCenter;
            bannerPanel.Controls.Add(bannerText);

            mainPanel = new Panel();
            mainPanel.Dock = DockStyle.Fill;
            mainPanel.BackColor = Color.White;

            this.Controls.Add(mainPanel);
            this.Controls.Add(bannerPanel);
        }

        private void ShowStep0()
        {
            currentStep = 0;
            mainPanel.Controls.Clear();

            titleLabel = new Label();
            titleLabel.Text = "Welcome to the AtoZ Scrapy Setup Wizard";
            titleLabel.Font = new Font("Segoe UI", 13, FontStyle.Bold);
            titleLabel.ForeColor = Color.FromArgb(0, 120, 212);
            titleLabel.Location = new Point(25, 25);
            titleLabel.Size = new Size(380, 30);

            descLabel = new Label();
            descLabel.Text = "This wizard will install AtoZ Scrapy Windows 11 ED (v0.0.1) on your computer.\n\nPlease select the destination folder for installation:";
            descLabel.Font = new Font("Segoe UI", 9.5f);
            descLabel.Location = new Point(25, 65);
            descLabel.Size = new Size(380, 50);

            Label pathLabel = new Label();
            pathLabel.Text = "Destination Folder:";
            pathLabel.Font = new Font("Segoe UI", 9, FontStyle.Bold);
            pathLabel.Location = new Point(25, 130);
            pathLabel.Size = new Size(380, 20);

            pathTextBox = new TextBox();
            pathTextBox.Text = installPath;
            pathTextBox.Font = new Font("Segoe UI", 9.5f);
            pathTextBox.Location = new Point(25, 155);
            pathTextBox.Size = new Size(280, 25);

            browseButton = new Button();
            browseButton.Text = "Browse...";
            browseButton.Location = new Point(315, 153);
            browseButton.Size = new Size(80, 27);
            browseButton.Click += BrowseButton_Click;

            nextButton = new Button();
            nextButton.Text = "Install ▶";
            nextButton.Font = new Font("Segoe UI", 9, FontStyle.Bold);
            nextButton.Location = new Point(305, 335);
            nextButton.Size = new Size(90, 30);
            nextButton.Click += NextButton_Click;

            cancelButton = new Button();
            cancelButton.Text = "Cancel";
            cancelButton.Location = new Point(205, 335);
            cancelButton.Size = new Size(90, 30);
            cancelButton.Click += (s, e) => this.Close();

            mainPanel.Controls.Add(titleLabel);
            mainPanel.Controls.Add(descLabel);
            mainPanel.Controls.Add(pathLabel);
            mainPanel.Controls.Add(pathTextBox);
            mainPanel.Controls.Add(browseButton);
            mainPanel.Controls.Add(nextButton);
            mainPanel.Controls.Add(cancelButton);
        }

        private void BrowseButton_Click(object sender, EventArgs e)
        {
            using (FolderBrowserDialog fbd = new FolderBrowserDialog())
            {
                fbd.SelectedPath = pathTextBox.Text;
                if (fbd.ShowDialog() == DialogResult.OK)
                {
                    pathTextBox.Text = fbd.SelectedPath;
                }
            }
        }

        private void NextButton_Click(object sender, EventArgs e)
        {
            installPath = pathTextBox.Text;
            ShowStep1();
        }

        private void ShowStep1()
        {
            currentStep = 1;
            mainPanel.Controls.Clear();

            titleLabel = new Label();
            titleLabel.Text = "Installing AtoZ Scrapy Windows 11 ED";
            titleLabel.Font = new Font("Segoe UI", 13, FontStyle.Bold);
            titleLabel.ForeColor = Color.FromArgb(0, 120, 212);
            titleLabel.Location = new Point(25, 25);
            titleLabel.Size = new Size(380, 30);

            statusLabel = new Label();
            statusLabel.Text = "Copying program files to destination...";
            statusLabel.Font = new Font("Segoe UI", 9.5f);
            statusLabel.Location = new Point(25, 75);
            statusLabel.Size = new Size(380, 25);

            progressBar = new ProgressBar();
            progressBar.Location = new Point(25, 110);
            progressBar.Size = new Size(370, 25);
            progressBar.Style = ProgressBarStyle.Blocks;
            progressBar.Value = 10;

            mainPanel.Controls.Add(titleLabel);
            mainPanel.Controls.Add(statusLabel);
            mainPanel.Controls.Add(progressBar);

            Thread installThread = new Thread(PerformInstallation);
            installThread.IsBackground = true;
            installThread.Start();
        }

        private void PerformInstallation()
        {
            try
            {
                Directory.CreateDirectory(installPath);
                UpdateProgress(30, "Copying application files & scripts...");
                Thread.Sleep(300);

                string downloadsFolder = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.UserProfile), "Downloads");
                string scrapyFolder = Path.Combine(downloadsFolder, "Scrapy");

                // Copy VBS and BAT scripts
                string sourceVbs = Path.Combine(scrapyFolder, "Start-AtoZ-Scrapy.vbs");
                string destVbs = Path.Combine(installPath, "Start-AtoZ-Scrapy.vbs");
                if (File.Exists(sourceVbs))
                {
                    File.Copy(sourceVbs, destVbs, true);
                }
                else
                {
                    File.WriteAllText(destVbs, "Set WshShell = CreateObject(\"WScript.Shell\")\r\nWshShell.Run \"pythonw.exe -m scrapy\", 0, False\r\n");
                }

                string sourceBat = Path.Combine(scrapyFolder, "Start-AtoZ-Scrapy.bat");
                string destBat = Path.Combine(installPath, "Start-AtoZ-Scrapy.bat");
                if (File.Exists(sourceBat))
                {
                    File.Copy(sourceBat, destBat, true);
                }
                else
                {
                    File.WriteAllText(destBat, "@echo off\r\npython -m scrapy\r\n");
                }

                // Copy compiled EXE if exists
                string sourceExe = Path.Combine(downloadsFolder, "AtoZ-Scrapy-Windows-11-ED.exe");
                if (!File.Exists(sourceExe))
                {
                    sourceExe = Path.Combine(scrapyFolder, "dist", "AtoZ-Scrapy-Windows-11-ED.exe");
                }
                string targetExe = Path.Combine(installPath, "AtoZ-Scrapy-Windows-11-ED.exe");
                if (File.Exists(sourceExe))
                {
                    try { File.Copy(sourceExe, targetExe, true); } catch { }
                }

                UpdateProgress(70, "Creating Desktop & Start Menu shortcuts...");
                Thread.Sleep(300);

                CreateShortcuts(destVbs, targetExe);

                UpdateProgress(100, "Installation Complete!");
                Thread.Sleep(300);

                this.Invoke(new Action(() => ShowStep2(destVbs, targetExe)));
            }
            catch (Exception ex)
            {
                this.Invoke(new Action(() => MessageBox.Show("Setup Warning: " + ex.Message, "Setup Notification", MessageBoxButtons.OK, MessageBoxIcon.Information)));
            }
        }

        private void UpdateProgress(int val, string status)
        {
            if (this.InvokeRequired)
            {
                this.Invoke(new Action(() => { progressBar.Value = val; statusLabel.Text = status; }));
            }
            else
            {
                progressBar.Value = val;
                statusLabel.Text = status;
            }
        }

        private void CreateShortcuts(string destVbs, string targetExe)
        {
            string desktop = Environment.GetFolderPath(Environment.SpecialFolder.Desktop);
            string onedriveDesktop = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.UserProfile), "OneDrive", "Desktop");
            string startMenu = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData), @"Microsoft\Windows\Start Menu\Programs");

            string shortcutDesktop = Path.Combine(desktop, "AtoZ Scrapy Windows 11 ED.lnk");
            string shortcutOneDrive = Path.Combine(onedriveDesktop, "AtoZ Scrapy Windows 11 ED.lnk");
            string shortcutStart = Path.Combine(startMenu, "AtoZ Scrapy Windows 11 ED.lnk");

            string script = string.Format(
                "$s = (New-Object -ComObject WScript.Shell).CreateShortcut('{0}'); $s.TargetPath = 'wscript.exe'; $s.Arguments = '\"{1}\"'; $s.WorkingDirectory = '{2}'; $s.Save(); " +
                "if (Test-Path '{3}') {{ $s1 = (New-Object -ComObject WScript.Shell).CreateShortcut('{4}'); $s1.TargetPath = 'wscript.exe'; $s1.Arguments = '\"{1}\"'; $s1.WorkingDirectory = '{2}'; $s1.Save(); }} " +
                "$s2 = (New-Object -ComObject WScript.Shell).CreateShortcut('{5}'); $s2.TargetPath = 'wscript.exe'; $s2.Arguments = '\"{1}\"'; $s2.WorkingDirectory = '{2}'; $s2.Save();",
                shortcutDesktop, destVbs, installPath, onedriveDesktop, shortcutOneDrive, shortcutStart
            );

            ProcessStartInfo psi = new ProcessStartInfo("powershell", "-Command \"" + script + "\"");
            psi.CreateNoWindow = true;
            psi.UseShellExecute = false;
            try
            {
                Process p = Process.Start(psi);
                p.WaitForExit();
            }
            catch { }
        }

        private void ShowStep2(string destVbs, string targetExe)
        {
            currentStep = 2;
            mainPanel.Controls.Clear();

            bannerPanel.BackColor = Color.FromArgb(40, 167, 69);

            titleLabel = new Label();
            titleLabel.Text = "Completing the AtoZ Scrapy Setup Wizard";
            titleLabel.Font = new Font("Segoe UI", 13, FontStyle.Bold);
            titleLabel.ForeColor = Color.FromArgb(40, 167, 69);
            titleLabel.Location = new Point(25, 25);
            titleLabel.Size = new Size(380, 30);

            descLabel = new Label();
            descLabel.Text = "AtoZ Scrapy Windows 11 ED has been successfully installed on your computer.\n\nShortcuts have been created on your Desktop and Start Menu.\n\nClick Finish to exit Setup.";
            descLabel.Font = new Font("Segoe UI", 9.5f);
            descLabel.Location = new Point(25, 65);
            descLabel.Size = new Size(380, 90);

            launchCheckBox = new CheckBox();
            launchCheckBox.Text = "Launch AtoZ Scrapy Windows 11 ED now";
            launchCheckBox.Font = new Font("Segoe UI", 9.5f, FontStyle.Bold);
            launchCheckBox.Checked = true;
            launchCheckBox.Location = new Point(25, 170);
            launchCheckBox.Size = new Size(350, 30);

            Button finishButton = new Button();
            finishButton.Text = "Finish ✔";
            finishButton.Font = new Font("Segoe UI", 9, FontStyle.Bold);
            finishButton.Location = new Point(305, 335);
            finishButton.Size = new Size(90, 30);
            finishButton.Click += (s, e) =>
            {
                if (launchCheckBox.Checked)
                {
                    try
                    {
                        ProcessStartInfo psi = new ProcessStartInfo("wscript.exe", "\"" + destVbs + "\"");
                        psi.WorkingDirectory = installPath;
                        Process.Start(psi);
                    }
                    catch
                    {
                        try
                        {
                            if (File.Exists(targetExe))
                            {
                                Process.Start(targetExe);
                            }
                        }
                        catch { }
                    }
                }
                this.Close();
            };

            mainPanel.Controls.Add(titleLabel);
            mainPanel.Controls.Add(descLabel);
            mainPanel.Controls.Add(launchCheckBox);
            mainPanel.Controls.Add(finishButton);
        }

        [STAThread]
        public static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new InstallerForm());
        }
    }
}
