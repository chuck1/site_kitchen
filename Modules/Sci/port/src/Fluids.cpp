#include <Fluids.hpp>

//char const * modules_dir = "nfs/stak/students/r/rymalc/Documents/Programming/Python/Modules/";
//char const * media_dir = "nfs/stak/students/r/rymalc/Documents/Programming/Python/Modules/Sci/media/";

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
double	sum(std::vector<double> a) {
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

Poly::Poly() {
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
double				Poly::eval(double X) {
	//print "X",X

	std::vector<double> Y(X, a_.size());
	//auto Y = np.array( [X]*len(self.a) );

	auto z = sum( mul(a_, pow( Y, range(a_.size())) ));

	return z;
}
std::vector<double>		Poly::eval(std::vector<double> X) {
	//print "X",X
	std::vector<double> Z;
	for(auto x : X) {

		Z.push_back(eval(x));

	}
	return Z;
}
double		Poly::integrate(std::vector<double> X) {
	auto Y = eval(X);
	auto Z = integ(X, Y);
	return Z;
}

Property::Property() {
	//print 'prop tag=',node.tag

	/*for(child in list(node)) {
	  self.poly.append( Poly( child ) );
	  }*/

}

Fluid::Fluid(std::string filename) {

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
void					Fluid::save(std::string filename) {

	std::ofstream ofs;
	ofs.open(filename);
	boost::archive::xml_oarchive ar(ofs);

	serialize(ar,0);

}
Fluid::Fluid() {}
double		Fluid::get(std::string prop_name, double T) {
	auto it = props_.find(prop_name);

	if(it == props_.end()) {
		list();
		throw 0;
	}

	Property& prop = it->second;

	auto poly = prop.polys_[0];

	return poly.eval( T );
}
void		Fluid::list() {
	//"""list properties"""
	for(auto it : props_) {
		std::cout << it.first << std::endl;
	}
}
double		Fluid::enthalpy_change(double T0, double T1) {
	auto X = linspace(T0,T1,100);

	return props_["cp"].polys_[0].integrate( X );
}
double		Fluid::get_Pr(double T) {
	auto cp = get("cp",T);
	auto mu = get("dynamic_viscosity",T);
	auto k = get("thermal_conductivity",T);

	//print cp,mu,k;

	auto Pr = cp * mu / k;
	return Pr;
}


