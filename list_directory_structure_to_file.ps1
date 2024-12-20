# Define the base directory and output file
$baseDir = "C:\Users\NicolasArgenteAIQOS\OneDrive - AIQOS B.V\Documents\GitHub\SnipSet"
$outputFile = "directory_structure.txt"
$maxDepth = 4  # Set the maximum depth you want to display

# Function to get directory structure up to a specified depth
function Get-DirectoryStructure {
    param (
        [string]$path,
        [int]$currentDepth,
        [int]$maxDepth
    )

    $items = Get-ChildItem -Path $path
    $output = @()

    foreach ($item in $items) {
        $indent = "│   " * ($currentDepth - 1)
        if ($currentDepth - 1 -eq 0) {
            $output += $indent + $item.Name
        } else {
            $output += $indent + "├───" + $item.Name
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
$output += Get-DirectoryStructure -path $baseDir -currentDepth 1 -maxDepth $maxDepth

# Write the output to a file
$output | Out-File -FilePath $outputFile

Write-Output "Directory structure saved to $outputFile"
