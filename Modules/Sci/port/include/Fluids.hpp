#include <vector>
#include <cassert>
#include <cmath>
#include <memory>
#include <map>
#include <fstream>

#include <boost/serialization/nvp.hpp>
#include <boost/serialization/map.hpp>
#include <boost/serialization/shared_ptr.hpp>

#include <boost/archive/xml_iarchive.hpp>


/*import os
  import math
  import re
  import sys
  from lxml import etree
  import numpy as np*/

//modules_dir = os.environ["HOME"] + '/Documents/Programming/Python/Modules/'
//media_dir = modules_dir + 'Sci/media/'

char const * modules_dir = "nfs/stak/students/r/rymalc/Documents/Programming/Python/Modules/";
char const * media_dir = "nfs/stak/students/r/rymalc/Documents/Programming/Python/Modules/Sci/media/";


/*void get_child_by_attr(root,attr,value) {
  for child in list(root) {
  if(child.get(attr) == value)
  return child;
  }
  return None;
  }*/
/*
   void process_element(root) {
//print root.tag
for child in list(root):
process_element(child)
}
*/

std::vector<int>	range(int stop) {
	std::vector<int> ret;
	for(int i = 0; i < stop; i++) {
		ret.push_back(i);
	}
	return ret;
}
std::vector<double>	linspace(double a, double b, int n) {
	std::vector<double> ret;
	for(int i = 0; i < n; ++i) {
		ret.push_back(a + (b-a)/((double)(n-1)) * ((double)i));
	}
	return ret;
}
std::vector<double>	mul(std::vector<double> a, std::vector<double> b) {
	assert(a.size() == b.size());
	std::vector<double> ret;
	for(auto i : range(a.size())) {
		ret.push_back(a[i] * b[i]);
	}
	return ret;
}
double			sum(std::vector<double> a) {
	double ret = 0;
	for(auto d : a) {
		ret += d;
	}
	return ret;
}
std::vector<double>	pow(std::vector<double>& a, std::vector<int> b) {
	assert(a.size() == b.size());
	std::vector<double> ret;
	for(auto i : range(a.size())) {
		ret.push_back(pow(a[i], b[i]));
	}
	return ret;
}

double	integ(std::vector<double>X, std::vector<double> Y) {
	double ret = 0;
	for(unsigned int i = 1; i < X.size(); i++) {
		ret += ((Y[i] + Y[i-1]) * (X[i] - X[i-1]) * 0.5);
	}
	return ret;
}

class Poly {
	public:
		Poly() {
			/*		text = node.text;
					text = re.sub('[\s\n]*','',text);
					split = re.split(",", node.text);*/

			//		self.a = np.array([]);

			//print 'poly tag =', node.tag, "attr =",node.attrib

			//print 'poly text=%r' % node.text
			//print 'split {0}'.format( split )

			// process coefficients
			/*		for(s in split) {
					v = float(s);
					self.a = np.append(self.a, v);*/
			//	}

			//print "a =",self.a
		}
		template<typename Archive> void		serialize(Archive & ar, unsigned int const & version) {
			ar & boost::serialization::make_nvp("a", a_);
		}
		double				eval(double X) {
			//print "X",X

			std::vector<double> Y(X, a_.size());
			//auto Y = np.array( [X]*len(self.a) );

			auto z = sum( mul(a_, pow( Y, range(a_.size())) ));

			return z;
		}
		std::vector<double>		eval(std::vector<double> X) {
			//print "X",X
			std::vector<double> Z;
			for(auto x : X) {

				Z.push_back(eval(x));

			}
			return Z;
		}
		double		integrate(std::vector<double> X) {
			auto Y = eval(X);
			auto Z = integ(X, Y);
			return Z;
		}

		/**
		 * polynomial coefficients
		 */
		std::vector<double>	a_;
};
class Property {
	public:
		Property() {
			//print 'prop tag=',node.tag

			/*for(child in list(node)) {
			  self.poly.append( Poly( child ) );
			  }*/

		}
		template<typename Archive> void		serialize(Archive & ar, unsigned int const & version) {
			ar & boost::serialization::make_nvp("polys", polys_);
		}
		std::vector< Poly >		polys_;

};

class Fluid {
	Fluid(std::string filename) {

		filename = filename + ".xml";

		/*
		   tree = etree.parse( media_dir + filename );
		   root = tree.getroot();


		//print "parsing '{0}'".format(media_dir + filename)
		//print 'root tag=%r' % root.tag


		// process children
		for child in list(root) {
		name = child.get( 'name' );
		//print 'name=%r' % name

		if(name){
		self.dict[name] = Property( child );
		}
		}*/

		std::ifstream ifs;
		ifs.open(filename);
		boost::archive::xml_iarchive ar(ifs);

		serialize(ar,0);
	}
	template<typename Archive> void		serialize(Archive & ar, unsigned int const & version) {
		ar & boost::serialization::make_nvp("props", props_);
	}
	double		get(std::string prop_name, double T) {
		auto it = props_.find(prop_name);

		if(it == props_.end()) {
			list();
			throw 0;
		}

		Property& prop = it->second;

		auto poly = prop.polys_[0];

		return poly->eval( T );
	}
	void		list() {
		//"""list properties"""
		for(auto it : props_) {
			std::cout << it.first << std::endl;
		}
	}
	double		enthalpy_change(double T0, double T1) {
		auto X = linspace(T0,T1,100);

		return props_["cp"].polys_[0]->integrate( X );
	}
	double		get_Pr(double T) {
		auto cp = get("cp",T);
		auto mu = get("dynamic_viscosity",T);
		auto k = get("thermal_conductivity",T);

		//print cp,mu,k;

		auto Pr = cp * mu / k;
		return Pr;
	}

	std::map< std::string, Property >	props_;
};




/*void np_array(X) {
	if not isinstance(X,np.ndarray):
		if isinstance(X,list) {
			X = np.array(X);
		}
		else {
			X = np.array([X]);
		}
	return X;
}*/
/*
void frange(start,stop,step) {
	r = start;
	x = np.array(());
	while(r <= stop) {
		x = np.append(x,r);
		r += step;
	}
	return x;
}*/
/*
   if __name__ == "__main__":
   import Sci.Fluids
   help(Sci.Fluids)

   f = Sci.Fluids.Fluid('co2')
   f.list()

*/
