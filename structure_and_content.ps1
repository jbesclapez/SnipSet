# Define variables at the top
$baseDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$outputFile = "structure_and_content.txt"
$maxDepth = 4  # Set the maximum depth you want to display
$excludedDirs = @("__pycache__", "migration", "frontend", "db_data", ".git")
$contentExtensions = @(".yml", ".sh", ".py")
$contentFilenames = @("dockerfile", "readme.md")

# Function to get directory structure up to a specified depth
function Get-DirectoryStructure {
    param (
        [string]$path,
        [int]$currentDepth,
        [int]$maxDepth
    )

    $items = Get-ChildItem -Path $path | Where-Object {
        # Exclude directories we don't want to display
        if ($_.PSIsContainer) {
            $_.Name -notin $excludedDirs
        } else {
            $true
        }
    }

    $output = @()

    foreach ($item in $items) {
        # Use a simple ASCII indentation
        $indent = ("  " * ($currentDepth - 1))
        if ($currentDepth - 1 -eq 0) {
            $output += ($indent + $item.Name)
        } else {
            $output += ($indent + "|---" + $item.Name)
        }

        if ($item.PSIsContainer -and $currentDepth -lt $maxDepth) {
            $subItems = Get-DirectoryStructure -path $item.FullName -currentDepth ($currentDepth + 1) -maxDepth $maxDepth
            $output += $subItems
        }
    }
    return $output
}

# Initialize output with the base directory
$output = @($baseDir)

# Get the directory structure
$structure = Get-DirectoryStructure -path $baseDir -currentDepth 1 -maxDepth $maxDepth

# Write the initial directory structure to file
($output + $structure) | Out-File -FilePath $outputFile -Encoding UTF8

# After listing structure, retrieve the content of the specified files
# We'll find all files that match our criteria and are not in excluded directories, including root folder.
$allFiles = Get-ChildItem -Path $baseDir -Recurse -File | Where-Object {
    $fullPath = $_.FullName

    # Check if file is in an excluded directory
    $excludeFile = $false
    foreach ($exdir in $excludedDirs) {
        if ($fullPath -match ("\\$exdir($|\\)")) {
            $excludeFile = $true
            break
        }
    }

    if ($excludeFile) {
        $false
    } else {
        ($contentExtensions -contains [System.IO.Path]::GetExtension($_.Name).ToLower()) -or
        ($contentFilenames -contains $_.Name.ToLower())
    }
}

# Include root folder files
$rootFiles = Get-ChildItem -Path $baseDir -File | Where-Object {
    ($contentExtensions -contains [System.IO.Path]::GetExtension($_.Name).ToLower()) -or
    ($contentFilenames -contains $_.Name.ToLower())
}
$allFiles += $rootFiles

Add-Content -Path $outputFile -Value "`r`n"
foreach ($file in $allFiles) {
    Add-Content -Path $outputFile -Value "**** Here is the content of the file in the path $($file.FullName)"
    Add-Content -Path $outputFile -Value (Get-Content $file.FullName -Raw)
    Add-Content -Path $outputFile -Value "`r`n"
}

Write-Output "Directory structure and file contents saved to $outputFile"