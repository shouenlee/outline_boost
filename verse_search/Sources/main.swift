import Foundation
var basePath = Bundle.main.bundlePath

#if DEBUG
print("Debug mode")
basePath = FileManager.default.currentDirectoryPath
#endif

//print(basePath)
var searchTerm = CommandLine.arguments.popLast()
let fnSearch: Bool

if searchTerm == "-f" {
    fnSearch = true
    searchTerm = CommandLine.arguments.popLast()
} else {
    fnSearch = false
}

let terminalArguments: Array<String> = Array(CommandLine.arguments) // There is always one argument passed, which is the name of the program, we get rid of it here.
let joinedArguments: String = terminalArguments.joined(separator: " ").trimmingCharacters(in: .whitespacesAndNewlines)
var book: String = "*"
var chapter: String = "*"

do {
    (book, chapter) = try getBookFromArguments(arguments: terminalArguments)
} catch let errorType {
    print("There was a problem with your query: \(errorType)")
    exit(EXIT_FAILURE)
}

if let searchTerm = searchTerm {
    var grep_cmd: String
    if fnSearch {
        grep_cmd = basePath + "/Footnotes/" + book + "/" + chapter + "/*/*"
        grep_cmd = "for file in $(ls " + grep_cmd + "); do grep -i --color=always '" + searchTerm + "' $file; done"
        if book == "*" {
            for b in Set(books_map.values) {
                grep_cmd = "cat " + basePath + "/Footnotes/" + b + "/*/*/* | grep -i --color=always '" + searchTerm + "'"
                let ret = shell(command: grep_cmd)
                if !ret.isEmpty {
                    print(ret)
                }
            }
        } else {
            grep_cmd = "cat " + basePath + "/Footnotes/" + book + "/" + chapter + "/*/* | grep -i --color=always '" + searchTerm + "'"
            print(shell(command: grep_cmd))
        }
        
    } else {
        grep_cmd = "cat " + basePath + "/Verses/" + book + "/" + chapter + " | grep -i --color=always '" + searchTerm + "'"
        print(shell(command: grep_cmd))
    }
    print("testing")
} else {
    print("No search term specified")
    exit(EXIT_FAILURE)
}
