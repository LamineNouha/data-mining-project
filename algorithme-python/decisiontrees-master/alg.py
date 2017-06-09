"""
Implements the ID3 algorithm for the construction of
decision trees.

"""

"""
Implements a basic decision tree class, to be used in decision tree
construction algorithms.

"""

import csv
from collections import Counter


class DTree(object):
    """
    A decision tree object, consisting of a recursive set of decision tree
    nodes and basic parsing functions.

    """

    def __init__(self, training_file):
        """
        Initialize the decision tree from the given filename by parsing CSV
        data and setting necessary attributes.

        Args:
            filename: relative or absolute filepath to CSV file. CSV must
            follow format specified in README.
        Returns:
            An Decision Tree instance ready for learning with a decision tree
            creation algorithm.

        """
        self.training_file = training_file
        self.root = None
        self.parse_csv()
        self.get_distinct_values()

    def parse_csv(self, dependent_index=-1):
        """
        Set the object's attributes and data, where attributes is a list of
        attributes and data is an array of row dictionaries keyed by attribute.

        Also sets the dependent variable, which defaults to the last one. An
        option to change the position of this dependent variable has not yet
        been implemented.

        Args:
            dependent_index: the index to be specified as the dependent
                variable (default -1).
        Raises:
            NotImplementedError: If dependent_index is specified, since I
                haven't implemented that yet.

        """
        if dependent_index != -1:
            raise NotImplementedError

        reader = csv.reader(self.training_file)
        attributes = reader.next()
        data = []
        for row in reader:
            row = dict(zip(attributes, row))
            data.append(row)
        self.training_file.close()

        self.dependent = attributes[dependent_index]
        self.attributes = [a for a in attributes if a != self.dependent]
        self.all_attributes = attributes
        self.data = data

    def get_distinct_values(self):
        """
        Get the distinct values for each attribute in the CSV data.

        Returns:
            A dictionary with attribute keys and set values corresponding to
            the unique items in each attribute.

        """
        values = {}
        for attr in self.all_attributes:  # Use all attributes because ugly
            values[attr] = set(r[attr] for r in self.data)
        self.values = values

    def plot(self, x=1, y=1):
        """
        Recursively plot the given node and its children with matplotlib

        Args:
            x: the desired width of the plot (default 1).
            y: the desired height of the plot (default 1).
        Raises:
            NotImplementedError: Not yet implemented.

        """
        self.root._plot()

    def decide(self, attributes):
        """
        Make a decision on the dependent variable of the tree given the
        provided attributes.

        Args:
            attributes: the list of independent attributes, correctly ordered,
                with which to make a decision on the dependent value.
        Returns:
            A dependent variable representing the decision tree decision.
        Raises:
            ValueError: if an invalid property is found which is not
                represented in the decision tree.

        """
        if len(attributes) != len(self.attribute_order):
            print self.attribute_order
            raise ValueError("supplied attributes do not match data")
        attrs_dict = dict(zip(self.attribute_order, attributes))
        return self.root._decide(attrs_dict)

    def test_file(self, testing_file, csv=None):
        """
        Test the given CSV file on this instance's decision tree, either
        printing decisions to stdout or writing to a csv file.

        Note: Testing CSV files must have the same format as training CSV
        files, including column order. Repeated headers are optional.

        Args:
            testing_file: testing CSV file. Testing CSV files must have the
                same format as the training CSV files! this function will
                automatically close the file after usage.
            csv: if specified, will write to the given CSV file.

        """

        import csv
        reader = csv.reader(testing_file)
        first_row = reader.next()
        # If first row
        if first_row == self.all_attributes or first_row == self.attributes:
            test_data = []
        else:
            test_data = [dict(zip(self.all_attributes, first_row))]
        for row in reader:
            row = dict(zip(self.all_attributes, row))
            test_data.append(row)

        testing_file.close()

        correct = 0.  # Keep track of statistics
        for row in test_data:
            formatted = [row[a] for a in self.attributes]
            decision = self.decide(formatted)
            try:
                expected_str = "(expected {0})".format(row[self.dependent])
                if row[self.dependent] == decision:
                    correct += 1
                    expected_str += ", CORRECT"
                else:
                    expected_str += ", INCORRECT"
            except KeyError:
                expected_str = ""
            print "{0} -> {1} {2}".format(formatted, decision, expected_str)
        print "% correct: {0}".format(correct/len(test_data))

    def filter_subset(self, subset, attr, value):
        """
        Filter a subset of CSV data further by selecting only the rows of
        subset which have the given attribute and value.

        Args:
            subset: the subset of the CSV data to filter upon.
            attr: the attribute of the value to filter upon.
            value: the value to filter upon.
        Returns:
            A list of the filtered rows according to the attribute and value.

        """
        return [r for r in subset if r[attr] == value]

    def value_counts(self, subset, attr, value, base=False):
        """
        Get the number of currences per value of the dependent variable when
        the given attribute is equal to the given value.

        FIXME: Can attr/value be eliminated??

        Args:
            subset: the subset with which to act upon.
            attr: the attribute of the value.
            value: the value with which to track counts.
            base: whether or not to calculate values based on the dependent
                value (default False).
        Returns:
            A Counter instance detailing the number of occurrences per
            dependent variable.

        """
        counts = Counter()
        for row in subset:
            if row[attr] == value or base:
                counts[row[self.dependent]] += 1
        return counts

    def rules(self):
        """
        Return all of the node's tree branch traversals, which
        can be used as if/then rules for simulating the decision process.

        Returns:
            A 2d list of all known tree branch traversals.

        """
        return sorted(
            self.root._rules(),
            key=lambda t: (len(t), [p[1] for p in t if isinstance(p, tuple)])
        )

    def set_attributes(self, attributes):
        """
        Set the correct order of the attributes in the decision tree
        based on the parsed CSV data.

        Args:
            attributes: the correctly ordered list of independent attributes
                from the CSV data.

        """
        self.attribute_order = attributes

    def attr_counts(self, subset, attr):
        """
        Get the number of occurrences per value of the given attribute

        Args:
            subset: the subset with which to act upon.
            attr: the selected attribute.
        Returns:
            A Counter instance detailing the number of occurrences per
            attribute value.

        """
        counts = Counter()
        for row in subset:
            counts[row[attr]] += 1
        return counts

    @property
    def depth(self):
        """
        Return the maximum depth of the tree assuming the current node
        as the parent.

        Returns:
            An integer calculated from the longest tree branch traversal.

        """
        return self.root._depth(0)

    @property
    def num_leaves(self):
        """
        Return the total number of leaves for the current tree.

        Returns:
            An integer of the number of leaves.

        """
        # FIXME: Not safe for an ID3 for which tree has not been created
        if self.root.leaf:
            return 1
        else:
            return sum(c._num_leaves for c in self.root.children)

    @property
    def distinct_values(self):
        """
        Returns a readable list of all values in the CSV data set.

        Returns:
            A flattened list of all distinct values.

        """
        values_list = []
        for s in self.values.values():
            for val in s:
                values_list.append(val)
        return values_list

    def __str__(self):
        """
        Return the filename of the decision tree, the dependent variable, and
        the string representation of the decision tree decision tree.

        """
        return "decision tree for {0}:\nDependent variable: {1}\n{2}".format(
            self.training_file.name,
            self.dependent,
            self.root
        )

    def __repr__(self):
        """
        Return the filename of the decision tree and other useful diagnostics.

        """
        return ("decision tree for {0}:\nDependent variable: {1}\n{2}\n" +
                "Rows: {3}\nValues: {4}\nBase Data Entropy: {5}\n ").format(
            self.training_file.name,
            self.dependent,
            repr(self.root),
            len(self.data),
            self.values,
            self.get_base_entropy(self.data)
			
        )

    def decision_repl(self,values):
        """
        An interactive REPL for making decisions based on the created decision
        tree.

        """
        print
       # print ','.join("{{{0}}}".format(a) for a in self.attributes)
        print "Decision tree REPL. Enter above parameters separated by commas,"
        print "no spaces between commas or brackets."
        #while True:
           # x = raw_input('> ').split(',')
		#testing_file=values.split(',')
         #   print "{0} ->".format(x)
         #   try:
		#file=open('tt.txt','w')
		#file.write(self.decide(values.split(',')))
		#file.close()
		
        print self.decide(values.split(','))
          #  except Exception as e:
           #     print "Error with decision: {0}".format(e)


class DTreeNode(object):
    """
    A recursively defined decision tree node.

    """

    def __init__(self, label, parent_value=None, properties={}, leaf=False):
        """
        Initialize a decision tree node.

        Args:
            label: the label of the node, which can either be a decision
                attribute or a leaf result.
            parent_value: the name of the link from the current node to its
                parent (default None, used in cases of root nodes).
            properties: a JSON-like dictionary containing various diagnostic
                properties of the given node (e.g. information gain or entropy)
                (default empty dictionary).
            leaf: a boolean indicating whether or not this node is a leaf node
                (default False).
        """
        self.label = label
        self.children = []
        self.parent_value = parent_value
        self.properties = properties
        self.leaf = leaf

    def _plot(self, xoffset, yoffset):
        """
        Plot the given node at the xoffset and yoffset coordinates.

        Args:
            xoffset: the x coordinate for plotting of the given node.
            yoffset: the y coordinate for plotting of the given node.
        Raises:
            NotImplementedError: Not yet implemented.

        """
        raise NotImplementedError

    def _decide(self, attrs_dict):
        """
        Recursively decide using the given attribute/value dictionary.

        Internal function is separated from the more friendly decide() method.

        """
        if self.leaf:
            return self.label
        val = attrs_dict[self.label]
        for node in self.children:
            if val == node.parent_value:
                return node._decide(attrs_dict)
        raise ValueError("Invalid property found: {0}".format(val))

    def add_child(self, node):
        """
        Add the given child node to the list of children of the current node.

        Args:
            node: the DTree node to be appended as a child.

        """
        self.children.append(node)

    @property
    def num_children(self):
        """
        Return the total number of immediate child nodes under the current
        node.

        Returns:
            An integer of the number of children.

        """
        return len(self.children)

    @property
    def _num_leaves(self):
        """
        Return the total number of leaves that exist under the current node.

        """
        if self.leaf:
            return 1
        else:
            return sum(c.num_leaves for c in self.children)

    def _depth(self, init):
        """
        Accumulate the depth of the tree at the given node taking into
        account the previous depth of the tree.

        init is the existing depth accumulated from previous levels of the
        tree.

        """
        if self.leaf:
            return init
        else:
            return max(c._depth(init+1) for c in self.children)

    def _rules(self, parent=None, previous=()):
        """
        Return a 2d list of decision rules with the given parent node and
        the tuple of previous nodes.

        """
        # import pdb; pdb.set_trace()
        rows = []
        if parent is not None:
            previous += ((parent.label, self.parent_value), )
        if self.leaf:
            previous += ((self.label), )
            rows.append(previous)
        else:
            for node in self.children:
                rows.extend(node._rules(self, previous))
        return rows

    def __str__(self):
        """
        Recursively build a string representation of the tree starting at the
        current node.

        """
        return "--{0}--({1}, {2})".format(
            self.parent_value,
            self.label,
            ', '.join(str(c) for c in self.children)
        )

    def __repr__(self):
        """
        Recursively build a string representation of the tree starting at the
        current node. Differs from __str__ by including additional diagnostic
        information.

        """
        return "--{0}--({1} {2}, {3})".format(
            self.parent_value,
            self.label,
            self.properties,
            ', '.join(repr(c) for c in self.children)
        )

import math


class ID3(DTree):

    def create_tree(self, parent_subset=None, parent=None, parent_value=None,
                    remaining=None):
        """
        Recursively create the decision tree with the specified subset
        and node positions. Sets the created tree to self.dtree.

        Args:
            parent_subset: the subset of the data of the parent
                to create decision nodes on (defaut None, which is interpreted
                as using entire CSV data). This is further filtered down in the
                body of the function
            parent: the parent of the node to be created (default None, which
                sets the root of the dtree).
            parent_value: the name of the value connecting the parent node and
                the current node (default None).

        """

        # Identify the subset of the data used in the igain calculation
        if parent_subset is None:
            subset = self.data
        else:
            subset = self.filter_subset(parent_subset,
                                        parent.label,
                                        parent_value)

        if remaining is None:
            remaining = self.attributes

        use_parent = False
        counts = self.attr_counts(subset, self.dependent)
        if not counts:
            # Nothing has been found for the given subset. We label the node
            # based on the parent subset instead. This triggers the elif block
            # below
            subset = parent_subset
            counts = self.attr_counts(subset, self.dependent)
            use_parent = True

        # If every element in the subset belongs to one dependent group, label
        # with that group.
        if len(counts) == 1:  # Only one value of self.dependent detected
            node = DTreeNode(
                label=counts.keys()[0],
                leaf=True,
                parent_value=parent_value
            )
        elif not remaining or use_parent:
            # If there are no remaining attributes, label with the most
            # common attribute in the subset.
            most_common = max(counts, key=lambda k: counts[k])
            node = DTreeNode(
                label=most_common,
                leaf=True,
                parent_value=parent_value,
                properties={'estimated': True}
            )
        else:
            # Calculate max information gain
            igains = []
            for attr in remaining:
                igains.append((attr, self.information_gain(subset, attr)))

            max_attr = max(igains, key=lambda a: a[1])

            # Create the decision tree node
            node = DTreeNode(
                max_attr[0],
                properties={'information_gain': max_attr[1]},
                parent_value=parent_value
            )

        if parent is None:
            # Set known order of attributes for dtree decisions
            self.set_attributes(self.attributes)
            self.root = node
        else:
            parent.add_child(node)

        if not node.leaf:  # Continue recursing
            # Remove the just used attribute from the remaining list
            new_remaining = remaining[:]
            new_remaining.remove(node.label)
            for value in self.values[node.label]:
                self.create_tree(
                    parent_subset=subset,
                    parent=node,
                    parent_value=value,
                    remaining=new_remaining
                )

    def information_gain(self, subset, attr):
        """
        Calculate possible information gain from splitting the given subset
        with the specified attribute.

        Args:
            subset: the subset with which to calculate information gain.
            attr: the attribute used to calculate information gain.
        Returns:
            A float of the total information gain from the given split.

        """
        gain = self.get_base_entropy(subset)
        counts = self.attr_counts(subset, attr)
        total = float(sum(counts.values()))  # Coerce to float for division
        for value in self.values[attr]:
            gain += -((counts[value]/total)*self.entropy(subset, attr, value))
        return gain
		


    def get_base_entropy(self, subset):
        """
        Get overall entropy of the subset based on the dependent variable.

        Note: Although the current implementation of this ID3 algorithm only
        supports binary dependent variables, the code for base entropy is
        written (with a for loop, instead of a binary choice) so that it may
        be easily expanded to multivariate calculations later.

        Args:
            subset: the subset with which to calculate base entropy.
        Returns:
            A float of the base entropy.

        """
        return self.entropy(subset, self.dependent, None, base=True)

    def entropy(self, subset, attr, value, base=False):
        """
        Calculate the entropy of the given attribute/value pair from the
        given subset.

        Args:
            subset: the subset with which to calculate entropy.
            attr: the attribute of the value.
            value: the value used in calculation.
            base: whether or not to calculate base entropy based solely on the
                dependent value (default False).

        Returns:
            A float of the entropy of the given value.

        """
        counts = self.value_counts(subset, attr, value, base)
        total = float(sum(counts.values()))  # Coerce to float division
        entropy = 0
        for dv in counts:  # For each dependent value
            proportion = counts[dv] / total
            entropy += -(proportion*math.log(proportion, 2))
        return entropy


if __name__ == '__main__':
    import argparse
    import pprint
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument('training_file', type=argparse.FileType('r'),
                        help='name of the (training) .csv file')
	#parser.add_argument('values', help='values ici')
    parser.add_argument('-t', '--testing_file', nargs='?', const=None,
                        default=False, type=argparse.FileType('r'),
                        help='name of the testing .csv file')
    parser.add_argument('-d', '--decide', action='store_true',
                        help='enter decision REPL for the given tree')
    parser.add_argument('values', help='values ici')  # TODO: add CSV support

    args = parser.parse_args()
    if args.testing_file is None:
        sys.exit('id3.py: error: testing file not specified')

    id3 = ID3(args.training_file)
    id3.create_tree()
    print repr(id3)

   # if args.rules:
     #   pprint.pprint(id3.rules(), width=400)

    if args.testing_file:
        id3.test_file(args.testing_file)

    if args.decide:
        id3.decision_repl(args.values)
