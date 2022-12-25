
#Class definition begins.
class PointDatabase:
    #Defining the node class
    class Node:
        def __init__(self, d=None):
            self.data = d
            self.left = None
            self.right = None
            self.parent=None
            self.ytree=None
 
    

# function to convert sorted array to a
# balanced BST
# input : sorted array of integers
# output: root node of balanced BST
#O(n).
#------------------------------------------------Functions assisting in construction--------------------------------------
    def sortedArrayToBST(self,arr):
     
        if not arr:
            return None
 
        # find middle index
        mid = (len(arr)) // 2
     
        # make the middle element the root
        root = self.Node(arr[mid])
     
        # left subtree of root has all
        # values <arr[mid]
        root.left = self.sortedArrayToBST(arr[:mid])
        
     
        # right subtree of root has all
        # values >arr[mid]
        root.right = self.sortedArrayToBST(arr[mid+1:])
        
        return root
    #To ensure that each node is connected to its parent. O(n).
    def connect_parents(self, root):
        
        if root.left:
            root.left.parent=root
            self.connect_parents(root.left)
        if root.right:
            root.right.parent=root
            self.connect_parents(root.right)
    
    #Takes a list of tuples, if the x value of tuple is less than key append to yleft, else if larger append to yright. O(n).    
        
    def sortby_y(self,L, key):
        yleft=[]
        yright=[]
        for c in L:
            if c<key:
                yleft.append(c)
            elif c>key:
                yright.append(c)
        return yleft, yright
#----------------------------------------------------------Builder Function------------------------------------------------------------  
#Recursively builds balanced bst(range tree), given a list which is first sorted by x, and then by y. This has time complexity O(nlogn), since recursion
#causes the function to split the problem in half each time, so function is called logn times, and each call has roughly O(n) operations.
    def build_2d_range_tree(self, xl, yl):
        T_assoc=self.sortedArrayToBST(yl)
        self.connect_parents(T_assoc)
        
        if len(xl)==1:
            v=self.Node(xl[0])
            v.ytree=T_assoc
            
        elif len(xl)==2:
            v=self.Node(xl[1])
            v.left=self.Node(xl[0])
            v.left.ytree=v.left
            v.left.parent=v
            v.ytree=T_assoc
            
        else:
            md=(len(xl))//2
            
            xmd=xl[md]
            xleft=xl[0:md]
            xright=xl[md+1::]
            yleft, yright=self.sortby_y(yl, xmd)
            
            v_left=self.build_2d_range_tree(xleft, yleft)
            v_right=self.build_2d_range_tree(xright, yright)
            v=self.Node(xmd)
            v.left=v_left
            
            v.right=v_right
            
            v.ytree=T_assoc
            
        return v
#-------------------------------------------------------------------Debugging Functions-----------------------------------------------------
    def printInOrder(self, root):
        if root:
            if root.left:
                self.printInOrder(root.left)
            print(root.data)
            if root.right:
                self.printInOrder(root.right)
    def printLevelOrder(self, root):
        h = self.height(root)
        for i in range(1, h+1):
            self.printCurrentLevel(root, i)
 
 
    # Print nodes at a current level
    def printCurrentLevel(self, root, level):
        if root is None:
            return
        if level == 1:
            print([root.data,self.height(root)], end=" ")
        elif level > 1:
            self.printCurrentLevel(root.left, level-1)
            self.printCurrentLevel(root.right, level-1)
 
    def height(self, node):
        if node is None:
            return 0
        else:
        # Compute the height of each subtree
            lheight = self.height(node.left)
            rheight = self.height(node.right)
 
        # Use the larger one
            if lheight > rheight:
                return lheight+1
            else:
                return rheight+1

#------------------------------------------------------------------Constructor----------------------------------------------------------
#Returns length of positional database
    def __len__(self):
        return self._size
    #We sort the lists beforehand, with complexity nlogn. Moreover, build_2d_range_tree also has complexity nlogn, so overall complexity of init
    #remains O(nlogn).
    def __init__(self, pointlist):
        
        if pointlist==[]:
            self.tree=self.Node()
            self._size=0
        else:
            xlist=sorted(pointlist) #sort by x
            ylist=sorted(pointlist, key=lambda x: x[1]) #sort by y
            self._size=len(pointlist)
            self.tree=self.build_2d_range_tree(xlist, ylist)
            self.connect_parents(self.tree)
            
        
#-----------------------------------------------------Assisting search-query functions-------------------------------------------------    
    #Finds the first node with a value greater than or equal to t. Since root has values as tuples, we define a key parameter to be able to
    #decide basis of comparison. Worst case complexity is O(log n).
    def succ_search(self,t,root,key):
        
        if root==None:
            return
        else:
            terminal_node=root
            while root!=None:
                if root.data[key]==t:
                    terminal_node=root
                    break
                elif root.data[key]>t:
                    if root.left:
                        root=root.left
                    else:
                        terminal_node=root
                        break
                else:
                    if root.right:
                        root=root.right
                    else:
                        terminal_node=root
                        break
        while terminal_node.parent!=None:
            if terminal_node.data[key]>=t:
                
                return terminal_node
            else:
                terminal_node=terminal_node.parent
        if terminal_node.data[key]>=t:
            return terminal_node
        else:
            return

    
                
    #Finds the first node with a value less than or equal to t. Since root has values as tuples, we define a key parameter to be able to
    #decide basis of comparison. Worst case complexity is O(log n).
    def pred_search(self,t,root,key):
        if root==None:
            return
        else:
            terminal_node=root
            while root!=None:
                if root.data[key]==t:
                    terminal_node=root
                    break
                elif root.data[key]>t:
                    if root.left:
                        root=root.left
                    else:
                        terminal_node=root
                        break
                else:
                    if root.right:
                        root=root.right
                    else:
                        terminal_node=root
                        break
        while terminal_node.parent!=None:
            if terminal_node.data[key]<=t:
                return terminal_node
            else:
                terminal_node=terminal_node.parent
        if terminal_node.data[key]<=t:
            return terminal_node
        else:
            return
 
    
    #Finds least common ancestor of two given nodes. Since here both nodes are tuples, we have a key parameter which tells us whether to compare based on x
    #or y.
    def find_lca(self, root, v1, v2, key):
        if root is None or v1 is None or v2 is None:
            return None
 
    # If both n1 and n2 are smaller than root, then LCA
    # lies in left
        if(root.data[key] > v1.data[key] and root.data[key] > v2.data[key]):
            return self.find_lca(root.left, v1, v2, key)
 
    # If both n1 and n2 are greater than root, then LCA
    # lies in right
        if(root.data[key] < v1.data[key] and root.data[key] < v2.data[key]):
            return self.find_lca(root.right, v1, v2, key)
 
        return root


    #Returns the subtree rooted at root. Has complexity O(s) where s is size of subtree rooted at root.
    def list_subtree(self, root):
        L=[]
        if root:
            if root.left:
                L.extend(self.list_subtree(root.left))
            L.append(root.data)
            if root.right:
                L.extend(self.list_subtree(root.right))
        return L
#-------------------------------------------------------------Search Query functions-----------------------------------------------------

    #Searches for all nodes in the subtree rooted at "root",which lie between q-d to q+d. This has complexity O(log n+k) where n is size of tree rooted at
    #root, and k is the number of nodes inside range. We keep calling parent from v1 upto lca, and include all right subtrees of right parents of v1.
    #we include the right subtree of v1 too, and check all points on path between lca and v1. The process is repeated for lca and v2.
    def onedsearchquery(self,root,q,d):
        M=[]
        if root==None:
            return M
        check=root.ytree.parent
        root.ytree.parent=None
        
        v1=self.succ_search(q-d, root.ytree,1)
        v2=self.pred_search(q+d, root.ytree,1)
        lca=self.find_lca(root.ytree,v1,v2,1)
        
        if lca==None:
            root.ytree.parent=check
            return M
        if v1.data[1]>q+d and v2.data[1]<q-d:
            root.ytree.parent=check
            return M
        else:
            
            v=v1
            while v!=lca:
                if v.data[1]>=q-d and v.data[1]<=q+d:
                    M.append(v.data)
                if v==v.parent.left and v.parent.right:
                    if v.parent!=lca:
                        M.extend(self.list_subtree(v.parent.right))
                v=v.parent
                
            v=v2
            while v!=lca:
                if v.data[1]>=q-d and v.data[1]<=q+d:
                    M.append(v.data)
                if v==v.parent.right and v.parent.left:
                    if v.parent!=lca:
                        M.extend(self.list_subtree(v.parent.left))
                v=v.parent
                
            if lca.data[1]>=q-d and lca.data[1]<=q+d:
                M.append(lca.data)
            if v1!=lca and (v1.right):
                M.extend(self.list_subtree(v1.right))
            if v2!=lca and v2.left:
                M.extend(self.list_subtree(v2.left))
        root.ytree.parent=check
        return M



    #This function searches the x-tree for points which fall in the x range. Then it queries the y-trees of such points, using onedrangequery()
    #to get the final answer. Complexity is O(log^2 n+m), as demanded.
    
        

    def searchNearby(self, q, d):
        L=[]
        
        if len(self)==0:
            return L
        v1=self.succ_search(q[0]-d, self.tree,0)
        v2=self.pred_search(q[0]+d, self.tree,0)
        lca=self.find_lca(self.tree,v1,v2,0)
        
        if lca==None:
            return L
        if v1.data[0]>q[0]+d:
            return L
        elif v2.data[0]<q[0]-d:
            return L
        
        else:
            v=v1
            while v!=lca:
                if v.data[0]>=q[0]-d and v.data[0]<=q[0]+d:
                    if v.data[1]>=q[1]-d and v.data[1]<=q[1]+d:
                        L.append(v.data)
                if v==v.parent.left and v.parent.right:
                    if v.parent!=lca:
                        L.extend(self.onedsearchquery(v.parent.right, q[1],d))
                    v=v.parent
                else:
                    v=v.parent
            v=v2
            
            while v!=lca:
                
                if v.data[0]>=q[0]-d and v.data[0]<=q[0]+d:
                    if v.data[1]>=q[1]-d and v.data[1]<=q[1]+d:
                        L.append(v.data)
                       
                if v==v.parent.right and v.parent.left:
                    if v.parent!=lca:
                        L.extend(self.onedsearchquery(v.parent.left, q[1],d))
                    v=v.parent
                
                    
                    
                else:
                    v=v.parent
            if lca.data[0]<=q[0]+d and lca.data[0]>=q[0]-d:
                if lca.data[1]<=q[1]+d and lca.data[1]>=q[1]-d:
                    L.append(lca.data)
            if v1!=lca and (v1.right):
                L.extend(self.onedsearchquery(v1.right, q[1],d))
            if v2!=lca and v2.left:
                L.extend(self.onedsearchquery(v2.left, q[1],d))
        
        return L

