#!/usr/bin/env python
# -*- coding: utf-8 -*-


# import needed libraries
import os
import os.path

from typing import Dict, Tuple


# TODO: (1) Need to add checks to ensure that user input is correct + currently only works for ontology and class data

class DocumentationMaker(object):
    """Has functionality to interact with a user and gather the information needed in order to prepare the input
    documents needed to run the PheKnowLator program. For more information on the dependency documents, please see
    the following Wiki: https://github.com/callahantiff/PheKnowLator/wiki/Dependencies.

    If successfully run, the class will write the following three documents to the ./resources directory:
        1. resource_info.txt
        2. ontology_source_list.txt
        3. edge_source_list.txt

    Attributes:
        edge_count: An integer specifying the number of edges to create.
        write_location: A string containing a filename. Defaults to './resources'.

    Raises:
        ValueError: If edge_count is not an integer.
    """

    def __init__(self, edge_count: int, write_location: str = './resources') -> None:

        # check edge count
        if not isinstance(edge_count, int): raise ValueError('edge_count must be an integer (i.e. "1" not "one").')
        else: self.edge_count = edge_count

        # make sure that the specified location to write data exists
        if os.path.exists(write_location):
            self.write_location = write_location
        else:
            print('Creating {} directory.'.format(write_location))
            os.mkdir('./resources/')
            self.write_location = write_location

    def information_getter(self) -> Tuple[Dict[str, str], Dict[str, str], Dict[str, str]]:
        """Creates three dictionaries from information provided by a user. The three dictionaries store information
        for each of the two required documents.

        Returns:
            A list of two dictionaries:
                1. Information needed to create the resource_info.txt file.
                2. Information needed to create the ontology_source_list.txt file.
                3. Information needed to create the edge_source_list.txt file.
        """

        # store input
        resource_data, ont_data, edge_data = {}, {}, {}

        # get edge information
        for edge in range(self.edge_count):
            print('\n' + '#' * 40)
            print('GATHERING INFORMATION FOR EDGE: {count}/{total}'.format(count=edge, total=self.edge_count))
            print('#' * 40)

            edge_name = input('Please enter the edge type (e.g. "gene-protein", "disease-chemical"): ')
            print('\n')

            ont = input('Is one or both of the nodes in edge an ontology? Please enter "one" or "both": ')
            if ont == 'one':
                ont_edge = input('Enter node name for ontology (e.g. "go"): ')
                ont_data[ont_edge] = input('Provide an owl or obo URL for this ontology: ')
            else:
                for _ in range(2):
                    ont_edge = input('Enter node name for ontology (e.g. "go"): ')
                    ont_data[ont_edge] = input('Provide an owl or obo URL for this ontology: ')

            print('\n')
            data_type = input('Provide the data types for each node in the edge (e.g. "class" or "entity" (for '
                              'non-class data) each node in the edge separated by "-" --> "class-entity"): ')
            print('\n')

            delimiter = input('Provide the character used to split each row into columns (e.g. "t" or ","): ')
            print('\n')

            col_idx = input('Provide the column index for each node in the input data, separated by ";" (e.g. "0;3"): ')
            print('\n')

            id_maps = input('Provide identifier mapping information for each node: col:./filepath '
                            '(col = edge[node_idx], filepath = mapping data location)\n'
                            '  - If both nodes require mapping, separate each set of mapping information by a ";" '
                            '(e.g. "0:./filepath;1:./filepath")\n'
                            '  - If none of the nodes require mapping, please enter "None"\nProvide mapping '
                            'information now: ') or 'None'
            print('\n')
            evi_crit = input('Provide evidence column information needed to filter edges: (e.g. keep all rows from the '
                             '3rd column that contain "IEA": "4;==;IEA")\n'
                             '  - If there are multiple evidence columns, separate each set of information by "::" '
                             '(e.g. "4;!=;IEA::6;>;0")\n'
                             '  - If there are no evidence columns, please enter "None"\nProvide evidence information '
                             'now: ') or 'None'
            print('\n')
            filt_crit = input('Provide filtering column information needed to filter edges: (e.g. keep all rows '
                              'starting with "9606." from the 2nd column: 3;.startswith("9606.");'
                              '\n  - If there are multiple evidence columns, separate each set of information by "::" '
                              '(e.g. "3;.startswith("STRING");::7;==;Homo sapiens")\n'
                              '  - If there are no evidence columns, please enter "None"\nProvide evidence '
                              'information now: ') or 'None'
            print('\n')
            edge_relation = input('Provide the Relation Ontology property class used to connect the nodes (e.g. '
                                  '"RO_0000056"): ')
            print('\n')

            subj_uri = input('Provide the Universal Resource Identifier that will be connected to the subject node ('
                             '(e.g. "http://purl.obolibrary.org/obo/"): ')
            print('\n')

            obj_uri = input('Provide the Universal Resource Identifier that will be connected to the object node: ')
            print('\n')

            source_label = input('Source Identifier Formatting (i.e. GO:12838340, when we need '
                                 'GO_12838340).\n\nProvide the following 3 items:\n(1) Character to split existing '
                                 'source labels (e.g. ":" in GO:1283834);\n(2) New label to replace existing label) '
                                 'for subject node (e.g. "GO_");\n(3) New label to replace existing label) for '
                                 'object node (e.g. GO_).\n\nEnter each item separated by ";". If the existing label '
                                 'is correct, press "enter": ') or ';;'
            print('\n')

            # add edge data to dictionary
            resource_data[edge_name] = '{0}|{1}|{2}|{3}|{4}|{5}|{6}|{7}|{8}|{9}'.format(source_label, data_type,
                                                                                        edge_relation, subj_uri,
                                                                                        obj_uri, delimiter, col_idx,
                                                                                        id_maps, evi_crit, filt_crit)

            # get edge data sources
            edge_data[edge_name] = input('Provide a URL or file path to data used to create this edge: ')

        return resource_data, ont_data, edge_data

    def writes_out_document(self, data: Dict[str, str], delimiter: str, filename: str) -> None:
        """Function takes a dictionary of file information and writes it to a user-provided location.

        Args:
            data: A dictionary of edge data.
            delimiter: A string containing a character to use as the row delimiter.
            filename: A string containing a file path.

        Returns:
            None
        """

        with open(self.write_location + '/' + filename, 'w') as outfile:
            for edge, values in data.items():
                outfile.write(edge + delimiter + values + '\n')
        outfile.close()

        return None


def main():

    # print initial message for user
    print('\n\n' + '***' * 50)
    print("\n".join((
        "INPUT DOCUMENT BUILDER",
        "",
        "This program will help you generate the input documentation needed to run PheKnowLator by asking specific information about each edge type in the knowledge graph.",
        "It will help you create three documents: (1) resource_info.txt; (2) ontology_source_info.txt; and (3) edge_source_info.txt.",
        "An example of the data this program expects to find within each of these documents is shown below:",
        "",
        "(1) resource_info.txt: This document represents each edge type as a single \"|\" delimited string and contains a total of 11 items:",
            "\t(1) Edge Type: A string containing a \"-\" delimited edge label (node1-node2)",
            "\t(2) Source Labels: 3 \";\"-delimited strings (e.g. \":;GO_;GO_)\":",
                "\t\t- the character to split existing labels (e.g. \":\" in GO:1283834)",
                "\t\t- a new label for the subject node",
                "\t\t- a new label for the object node. If the existing label is correct, use \";;\";",
            "\t(3) Data Type: A label of \"class\", \"entity\" ( for non-ontology data) provided for each node and separated by \"-\" (e.g. \"class-class\", \"class-entity\", \"entity-class\");",
            "\t(4) Edge Relation: A Relation Ontology identifier to be used as an edge between the nodes (e.g. \"RO_0000056\")",
            "\t(5) Subject URI: A Universal Resource Identifier that will be connected to the subject node in the Edge Type (e.g. \"http://purl.uniprot.org/geneid/\");",
            "\t(6) Object URI that will be connected to the object node in the Edge Type (e.g. \"http://purl.obolibrary.org/obo/\");",
            "\t(7) Delimiter: A character used to split input text rows into columns (e.g. \"t\" or \",\");",
            "\t(8) Column Indices: two column indices separated by \";\" (e.g. 0;4 for the first and third columns);",
            "\t(9) Identifier Maps: A string indicating the column index in the input data source needing identifier mapping and a file pointing to mapping data, for example:",
                "\t\t\"2:./resources/processed_data/mapping_file_1.txt;4:./resources/processed_data/mapping_file_2.txt\" means:",
                    "\t\t\t- mapping data from the first node in the edge to the 0th column in \"mapping_file_1.txt\"",
                    "\t\t\t- mapping data from the second node in the edge to the 4th column in \"mapping_file_2.txt\";",
            "\t(10) Evidence Criteria: Sets of 3 \"::\"-separated items, where each set is composed of three pieces of \";\"-separated information (e.g. \"4;!=;IEA::8;<;0.0001\" - means:",
                "\t\t\t- filter the 4th column to keep rows that do not contain \"IEA\"",
                "\t\t\t- filter the 8th column to keep rows with a value less than \"0.0001\";",
            "\t(11) Filter Criteria: Sets of 3 \"::\"-separated items, where each set is composed of three pieces of \";\"-separated information (e.g. \"5;==;P::7;==;9606\" - means:",
                "\t\t- filter the 5th column to only include rows with \"P\"",
                "\t\t- filter the 7th column to only include rows containing \"99606\"",
        "",
            "\tAn example line from the resource_info.txt file is shown below:",
                "\t\tchemical-gene|;MESH_;|class-class|;MESH_;|class-class|RO_0002434|http://purl.obolibrary.org/obo/|http://purl.uniprot.org/geneid/|#|t|1;4|0:./resources/data_maps/MESH_CHEBI_MAP.txt|None|7;==;9606",
        "",
        "(2) ontology_source_info.txt: This document contains a \",\"-delimited line for each ontology source used, for example:",
            "\t\"chemical,http://purl.obolibrary.org/obo/chebi.owl\"",
            "\t\"gene,http://purl.obolibrary.org/obo/so.owl\"",
        "",
        "(3) edge_source_info.txt: This document contains a \",\"-delimited line for each edge data source, for example:",
            "\t\"chemical-gene,http://ctdbase.org/reports/CTD_chem_gene_ixns.tsv.gz\"",
        "",
        "If you would like more information on the dependency documents need to run PheKnowLator, please visit the following Wiki page: https://github.com/callahantiff/PheKnowLator/wiki/Dependencies."
    )))
    print('***' * 50 + '\n')

    # initialize class
    edge_count = int(input('EDGE COUNT: Enter the number of edge types to create: '))
    edge_maker = DocumentationMaker(edge_count)

    # run method to obtain edge data information
    edge_data = edge_maker.information_getter()

    # write out resource info data
    print('***' * 12 + '\nWRITING REQUIRED INPUT DOCUMENTATION\n' + '***' * 12)
    edge_maker.writes_out_document(edge_data[0], '|', 'resource_info.txt')

    # write out ontology data
    edge_maker.writes_out_document(edge_data[1], ', ', 'ontology_source_list.txt')

    # write out edge data
    edge_maker.writes_out_document(edge_data[2], ', ', 'edge_source_list.txt')


if __name__ == '__main__':
    main()
