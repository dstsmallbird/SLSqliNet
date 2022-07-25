package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"strings"

	"github.com/pingcap/parser"
	"github.com/pingcap/parser/ast"
	_ "github.com/pingcap/parser/test_driver"
)

/*
* define Visitor as column name extractor:
ast.Node provides Accept(v Visitor)(node-node，ok-bool) to allow structure implementing ast.Visitor to traverse itself
*/
type colX struct {
	colNames []string
}

func (v *colX) Enter(in ast.Node) (ast.Node, bool) {
	if name, ok := in.(*ast.ColumnName); ok {
		v.colNames = append(v.colNames, name.Name.O)
	}
	return in, false
}

func (v *colX) Leave(in ast.Node) (ast.Node, bool) {
	return in, true
}

func extract(rootNode *ast.StmtNode) []string {
	v := &colX{}
	(*rootNode).Accept(v) // ast.Node's Accept funciton can traverse node
	return v.colNames
}

/*
* define Visitor as table name extractor
 */
type tabX struct {
	tableNames []string
}

func (v *tabX) Enter(in ast.Node) (ast.Node, bool) {
	if name, ok := in.(*ast.TableName); ok {
		v.tableNames = append(v.tableNames, name.Name.O)
	}
	return in, false
}

func (v *tabX) Leave(in ast.Node) (ast.Node, bool) {
	return in, true
}

func tableNameExtract(rootNode *ast.StmtNode) []string {
	v := &tabX{}
	(*rootNode).Accept(v)
	return v.tableNames
}

/*
 parse MySQL statements and return AST root node
*/
func parse(sql string) (*ast.StmtNode, error) {
	p := parser.New() // parser instance

	stmtNodes, _, err := p.Parse(sql, "", "") // parse MySQL statements
	if err != nil {
		return nil, err
	}

	return &stmtNodes[0], nil
}

/*
 Determine whether the file exists
*/
func checkFileIsExist(filename string) bool {
	if _, err := os.Stat(filename); os.IsNotExist(err) {
		return false
	}
	return true
}

/*
 read dataset, parse statements and extract column/table name
*/
func parse_file(filename_read string, filename_write string) {
	var file_write *os.File
	var err_write error

	// open dataset
	file_read, err := os.OpenFile(filename_read, os.O_RDWR, 0666)
	if err != nil {
		fmt.Println("Open file error!", err)
		return
	}
	defer file_read.Close()

	stat, err := file_read.Stat()
	if err != nil {
		panic(err)
	}
	var size = stat.Size()
	fmt.Println("file size=", size)

	// open writable file
	if checkFileIsExist(filename_write) { // determine whether the file exists
		file_write, err_write = os.OpenFile(filename_write, os.O_WRONLY, 0666)
		fmt.Println("文件存在")
	} else {
		file_write, err_write = os.Create(filename_write) //create file
		fmt.Println("文件不存在，故创建文件")
	}
	if err_write != nil {
		fmt.Println("需写入的文件打开失败:", err_write)
	}
	defer file_write.Close()

	// create reader
	buf := bufio.NewReader(file_read)
	count := 0

	for {
		// read one line
		line, err_read := buf.ReadString('\n')
		count++

		// parse current line and extract column/table name
		astNode, err_parse := parse(line)
		if err_parse != nil {
			fmt.Printf("parse error: %v\n", err_parse.Error())
			return
		}
		col_lists := extract((astNode))
		tab_lists := tableNameExtract((astNode))

		// write
		// concat str segments
		col_str := strings.Join(col_lists, " ")
		tab_str := strings.Join(tab_lists, " ")
		bytes_count, err_write := io.WriteString(file_write, col_str+" "+tab_str+"\n")
		if err_write != nil {
			fmt.Println("写入失败:", err_write)
		} else {
			fmt.Printf("[%d]写入完成，字节数：%d\n", count, bytes_count)
		}

		if err_read != nil {
			if err_read == io.EOF {
				fmt.Println("File read ok!")
				break
			} else {
				fmt.Println("Read file error!", err_read)
				return
			}
		}
	}
}

func main() {
	if len(os.Args) != 3 {
		fmt.Println("usage: colx 'read_file_path' 'write_file_path'")
		return
	}
	file_read := os.Args[1]
	file_write := os.Args[2]
	parse_file(file_read, file_write)
}
